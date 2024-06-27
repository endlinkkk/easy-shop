import pytest
from unittest.mock import patch
from catalog.models import Category, Product
from catalog.serializers import ProductSerializer
from rest_framework.response import Response


def test_get_products_popular(client, db):
    response: Response = client.get('/api/products/popular')
    assert len(response.data) == 1
    assert 'Тестовый продукт' == response.data[0]['title']


def test_create_product(client, db):
    category = Category.objects.get(id=1)
    product = Product.objects.create(category=category, price=100, count=5, date='2024-06-27', title="Тестовый продукт2", description="Описание тестового продукта2", fullDescription="Полное описание тестового продукта2", freeDelivery=True, rating=4.5)
    response: Response = client.get('/api/products/popular')
    assert len(response.data) == 2