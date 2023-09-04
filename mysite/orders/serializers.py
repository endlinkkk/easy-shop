from rest_framework import serializers
from .models import Basket, BasketItem, Order
from catalog.serializers import ProductSerializer


class ItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = BasketItem
        fields = [
            'product'
        ]


class BasketSerializer(serializers.ModelSerializer):

    items = ItemSerializer(many=True)

    class Meta:
        model = Basket
        fields = [
            'items'
        ]

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
        ]