from rest_framework import serializers
from .models import Basket, BasketItem
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