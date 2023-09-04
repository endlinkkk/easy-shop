from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Basket, BasketItem
from catalog.models import Product
from .serializers import BasketSerializer
from catalog.serializers import ProductSerializer

# Create your views here.

class BasketView(APIView):
    def get(self, request):
        basket, created = Basket.objects.get_or_create(user=request.user)
        basket_item = BasketItem.objects.filter(basket=basket)
        products = [item.product for item in basket_item]
        serialized = ProductSerializer(products, many=True)
        return Response(serialized.data)

    def post(self, request):
        data = request.data
        print('POST', data)
        product = Product.objects.get(id = data["id"])
        basket, created = Basket.objects.get_or_create(user=request.user)
        basket_item = BasketItem.objects.create(basket=basket, product=product, quantity=data['count'])
        serialized = ProductSerializer(product)
        serialized.data['reviews'] = len(serialized.data['reviews'])
        print(serialized.data)
        return Response(list(serialized.data))

    def delete(self, request):
        ...

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

