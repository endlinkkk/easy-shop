from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from cart.cart import Cart
from orders.models import Order
from catalog.models import Product
from .models import Payment
from .serializers import PaymentSerializer


class PaymentView(APIView):
    def change_the_count_of_products(self, order: Order):
        for item in order.products:
            product = Product.objects.get(id=item["id"])
            product.count -= item["count"]
            product.save()

    def post(self, request: HttpRequest, id: str) -> Response:
        order = Order.objects.get(id=id)
        data = request.data
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            Payment.objects.create(
                order=order,
                card_number=data["number"],
                name=data["name"],
                month=data["month"],
                year=data["year"],
                code=data["code"],
            )
            cart = Cart(request)
            cart.clear()
            order.status = "paid"
            order.save()
            self.change_the_count_of_products(order)
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)
