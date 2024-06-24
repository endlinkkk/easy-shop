import pytest
from unittest.mock import patch
from catalog.models import Product
from catalog.serializers import ProductSerializer
from rest_framework.response import Response


# TODO
# Перед запуском тестов создается БД с данными для тестов


@pytest.mark.django_db
def test_get_products_popular(client):
    response: Response = client.get('/api/products/popular')
    assert [] == response.data