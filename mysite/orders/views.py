from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from cart.cart import Cart
from .models import Order
from catalog.models import Product
from accounts.models import Profile
from .serializers import OrderSerializer, OrderIdSerializer
from catalog.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import json


class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        try:
            cart = Cart(request)
            serialized = cart.get_products()
            return Response(serialized.data)
        except:
            return Response([])

    def post(self, request: HttpRequest) -> Response:
        data = request.data
        product = Product.objects.get(id=data["id"])
        cart = Cart(request)
        if (product.count - data["count"]) < 0:
            return Response(status=400)
        cart.add(product, quantity=data["count"])
        serialized = cart.get_products()

        return Response(serialized.data)

    def delete(self, request: HttpRequest) -> Response:
        data = request.data
        cart = Cart(request)
        product = Product.objects.get(id=data["id"])
        cart.remove(product, data["count"])
        serialized = cart.get_products()
        return Response(serialized.data)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest) -> Response:
        order = Order.objects.filter(user=request.user)
        result = OrderSerializer(order, many=True).data
        return Response(result)

    def post(self, request: HttpRequest) -> Response:
        data = request.data
        products = []
        for product in data:
            products.append(product)
        order = Order.objects.create(user=request.user, products=products)
        return Response({"orderId": order.id})


class OrderIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get_totalCost(self, products: list[dict]) -> float:
        totalCost = 0
        for product in products:
            totalCost += float(product["price"]) * int(product["count"])
        return totalCost

    def get(self, request: HttpRequest, id: str) -> Response:
        order = Order.objects.get(id=id)
        result = OrderSerializer(order).data
        return Response(result)

    def post(self, request: HttpRequest, id: str) -> Response:
        order = Order.objects.get(id=id)
        order_data = request.data
        serializer = OrderIdSerializer(data=order_data)
        if serializer.is_valid():
            for field in order_data:
                setattr(order, field, order_data[field])
            order.status = "accepted"
            order.totalCost = self.get_totalCost(order_data["products"])
            order.save()
            return Response({"orderId": order.id})
        else:
            return Response(serializer.errors, status=400)
