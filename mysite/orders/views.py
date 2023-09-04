from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Basket, BasketItem, Order, OrderItem
from catalog.models import Product
from accounts.models import Profile
from .serializers import BasketSerializer, OrderSerializer
from catalog.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_products(basket_items) -> list:
        products = [item.product for item in basket_items]
        quantitys = [item.quantity for item in basket_items]
        serialized = ProductSerializer(products, many=True)
        for i, d in enumerate(serialized.data):
            d['count'] = quantitys[i]
            d['reviews'] = len(d['reviews'])
        return serialized.data

    def get(self, request):
        try:
            basket = Basket.objects.get(user=request.user)
            basket_item = BasketItem.objects.filter(basket=basket)
            data = BasketView.get_products(basket_item)
            return Response(data)
        except Basket.DoesNotExist:
            return Response([])
        

    def post(self, request):
        data = request.data
        print(data)
        product = Product.objects.get(id = data["id"])
        basket, created = Basket.objects.get_or_create(user=request.user)
        if created:
            print("Создали корзину")
            basket_item = BasketItem.objects.create(basket=basket, product=product, quantity=data['count'])
        else:
            basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
            if created:
                print('создали айтем')
                basket_item.product = product
                basket_item.quantity = data['count']
                basket_item.save()
            else:
                print('добавили к айтему')
                basket_item.quantity += data['count']
                basket_item.save()

        basket_item = BasketItem.objects.filter(basket=basket)
        data = BasketView.get_products(basket_item)
        return Response(data)

    def delete(self, request):
        data = request.data
        print(data)
        basket = Basket.objects.get(user=request.user)
        product = Product.objects.get(id=data["id"])
        print(product)
        basket_item = BasketItem.objects.get(basket=basket, product=product)
        print(basket_item)
        basket_item.quantity -= data['count']
        basket_item.save()
        if basket_item.quantity <= 0:
            print('должно удалить')
            basket_item.delete()

        basket_item = BasketItem.objects.filter(basket=basket)
        data = BasketView.get_products(basket_item)
        return Response(data)
    

    


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.get(user=request.user)
        order_items = [order_item.product for order_item in OrderItem.objects.filter(order=order)]
        order_serialized = OrderSerializer(order)
        order_items_serialized = ProductSerializer(order_items, many=True)
        order_serialized.data['products'] = order_items_serialized.data
        print(order_serialized.data)
        return Response(order_serialized.data)


    def post(self, request):
        data = request.data
        print(data)
        profile = Profile.objects.get(user=request.user)
        basket = Basket.objects.get(user=request.user)
        basket_items = BasketItem.objects.filter(basket=basket)
        total_cost = sum([basket_item.product.price for basket_item in basket_items])
        order, created = Order.objects.get_or_create(user=request.user,
                                                     fullName=profile.fullName,
                                                     email=profile.email,
                                                     phone=profile.phone,
                                                     deliveryType="free",
                                                     paymentType="online",
                                                     totalCost=total_cost,
                                                     status="accepted",
                                                     city="Moscow",
                                                     address="red square 1"
                                                     )
        for product in data:
            OrderItem.objects.create(order=order, product=Product.objects.get(id=product['id']), quantity=product['count'])
        
        return Response({"orderId": order.id})


class OrderIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        order = Order.objects.get(id=id)
        order_items = [order_item.product for order_item in OrderItem.objects.filter(order=order)]
        order_serialized = OrderSerializer(order)
        order_items_serialized = ProductSerializer(order_items, many=True)
        order_serialized.data['products'] = order_items_serialized.data
        print(order_serialized.data)
        return Response(order_serialized.data)

    def post(self, request, id):
        print(f"order post id {request.data}")
        data = request.data
        order = Order.objects.get(id=data['orderId'])
        order.deliveryType = data['deliveryType']
        order.paymentType = data['paymentType']
        order.status = data['status']
        order.city = data['city']
        order.address = data['address']
        order.save()
        return Response(status=200)

