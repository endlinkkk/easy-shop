from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Basket, BasketItem, Order
from catalog.models import Product
from accounts.models import Profile
from .serializers import BasketSerializer, OrderSerializer, OrderIdSerializer
from catalog.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json

# Исправить отображение оплаты и типа доставки (сейчас не отображается)

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
            if (product.count - data['count']) >= 0:
                basket_item = BasketItem.objects.create(basket=basket, product=product, quantity=data['count'])
            else:
                return Response(status=400)
        else:
            basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)
            if created:
                print('создали айтем')
                basket_item.product = product
                basket_item.quantity = data['count']
                if (product.count - basket_item.quantity) >= 0:
                    basket_item.save()
                else:
                    return Response(status=400)
            else:
                print('добавили к айтему')
                basket_item.quantity += data['count']
                print(basket_item.quantity)
                if (product.count - basket_item.quantity) >= 0:
                    basket_item.save()
                else:
                    return Response(status=400)

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
        order = Order.objects.filter(user=request.user)
        result = OrderSerializer(order, many=True).data
        print(result)
        return Response(result)

    def post(self, request):
        data = request.data
        products = []
        for product in data:
            products.append(product)
        order = Order.objects.create(user=request.user, products=products)
        return Response({"orderId": order.id})
    

class OrderIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get_totalCost(self, products):
        totalCost = 0
        for product in products:
            totalCost += float(product['price']) * int(product['count']) 
        return totalCost


    def get(self, request, id):
        order = Order.objects.get(id=id)
        result = OrderSerializer(order).data
        return Response(result)
    
    def post(self, request, id):
        order = Order.objects.get(id=id)
        order_data = request.data
        serializer = OrderIdSerializer(data=order_data)
        print(order_data)
        if serializer.is_valid():
            for field in order_data:
                setattr(order, field, order_data[field])
            order.status = 'accepted'
            order.totalCost = self.get_totalCost(order_data['products'])
            order.save()
            return Response({"orderId": order.id})
        else:
            return Response(serializer.errors, status=400)
