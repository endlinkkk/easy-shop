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

# class OrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Order
#         fields = [
#             'id',
#             'createdAt',
#             'fullName',
#             'email',
#             'phone',
#             'deliveryType',
#             'paymentType',
#             'totalCost',
#             'status',
#             'city',
#             'address',
#         ]

        
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
            'products',
         ]
        
class OrderIdSerializer(serializers.Serializer):
    fullName = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()

    def validate_fullName(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('fullName should be at least 2 characters long.')
        return value
    
    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('phone number must consist of numbers')
        return value
    
    def validate_city(self, value):
        if value.isdigit():
            raise serializers.ValidationError('The city name must not contain numbers')
        if len(value) < 2:
            raise serializers.ValidationError('Invalid city name')
        return value
    
    def validate_address(self, value):
        if len(value) < 5:
            raise serializers.ValidationError('Invalid address')
        return value