from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from .models import Payment
# Create your views here.


class PaymentView(APIView):
    # добавить валидацию и удаление корзины для пользователя
    def post(self, request, id):
        order = Order.objects.get(id=id)
        data = request.data
        print(data)
        Payment.objects.create(order=order,
                               card_number=data['number'],
                               name=data['name'],
                               month=data['month'],
                               year=data['year'],
                               code=data['code'])
        return Response(status=200)