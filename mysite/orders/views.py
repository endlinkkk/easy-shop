from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Basket, BasketItem
from catalog.models import Product
from .serializers import BasketSerializer
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
    def get(self, request):
        ...

    def post(self, request):
        ...


class OrderIdView(APIView):
    def get(self, request):
        ...

    def post(self, request):
        ...

