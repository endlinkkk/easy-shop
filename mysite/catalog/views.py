from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Product, Review, Tag
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    TagSerializer,
    SaleSerializer,
)
from .filters import products_filter
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Count
from datetime import date
from distutils.util import strtobool
import json


# Create your views here.
class CategoriesView(APIView):
    def get(self, request: HttpRequest):
        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class ProductIdView(APIView):
    def get(self, request: HttpRequest, id):
        product = get_object_or_404(Product, pk=id)
        serialized = ProductSerializer(product)
        return Response(serialized.data)


class ProductIdReviewView(APIView):
    def post(self, request: HttpRequest, id):
        product = get_object_or_404(Product, pk=id)
        data = request.data
        review = Review.objects.create(
            author=data["author"],
            email=data["email"],
            text=data["text"],
            rate=data["rate"],
            date=date.today(),
        )
        review.save()
        product.reviews.add(review)
        serialized = ReviewSerializer(review)
        return Response(serialized.data)


class TagView(APIView):
    def get(self, request: HttpRequest):
        tag = Tag.objects.all()
        serialized = TagSerializer(tag, many=True)
        return Response(serialized.data)


class CatalogView(APIView):
    def get(self, request: HttpRequest):
        current_page = request.GET.get("currentPage")
        products = products_filter(request)
        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(
            {"items": serialized.data, "current_page": current_page, "last_page": 10}
        )


class ProductPopularView(APIView):
    def get(self, request: HttpRequest):
        products = Product.objects.annotate(num_reviews=Count("reviews")).order_by(
            "-num_reviews", "-rating"
        )
        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(serialized.data)


class ProductLimitedView(APIView):
    def get(self, request: HttpRequest):
        products = Product.objects.filter(Q(count__gt=0), Q(count__lt=4))
        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(serialized.data)


class BannerView(APIView):
    def get(self, request: HttpRequest):
        products = Product.objects.all()
        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(serialized.data)


class SaleView(APIView):
    def get(self, request: HttpRequest):
        current_page = request.GET.get("currentPage")
        products = [product for product in Product.objects.all() if product.sale]
        serialized = SaleSerializer(products, many=True)
        return Response(
            {"items": serialized.data, "current_page": current_page, "last_page": 10}
        )
