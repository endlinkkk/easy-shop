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
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, F, Count
from datetime import date
from distutils.util import strtobool
import json


# Create your views here.
class CategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class ProductIdView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serialized = ProductSerializer(product)
        return Response(serialized.data)


class ProductIdReviewView(APIView):
    def post(self, request, id):
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
    def get(self, request):
        tag = Tag.objects.all()
        serialized = TagSerializer(tag, many=True)
        return Response(serialized.data)


class CatalogView(APIView):
    def get(self, request):
        d = {"inc": "-", "dec": ""}
        name = request.GET.get(
            "filter[name]"
        )  # Получение значения параметра filter[name]
        min_price = request.GET.get(
            "filter[minPrice]"
        )  # Получение значения параметра filter[minPrice]
        max_price = request.GET.get(
            "filter[maxPrice]"
        )  # Получение значения параметра filter[maxPrice]
        free_delivery = request.GET.get(
            "filter[freeDelivery]"
        )  # Получение значения параметра filter[freeDelivery]
        available = request.GET.get(
            "filter[available]"
        )  # Получение значения параметра filter[available]
        current_page = request.GET.get(
            "currentPage"
        )  # Получение значения параметра currentPage
        sort = request.GET.get("sort")  # Получение значения параметра sort
        sort_type = request.GET.get("sortType")  # Получение значения параметра sortType
        limit = request.GET.get("limit")
        # print(
        # f"name: {name}\nmin_price: {min_price}\nmax_price: {max_price}\nfree_delivery: {free_delivery}\navailable: {available}\ncurrent_page: {current_page}\nsort: {sort}\nsort_type: {sort_type}\nlimit: {limit}"
        # )
        products = Product.objects.all().order_by(f"{d[sort_type]}{sort}")

        if available == "true":
            avail_filter = Q(count__gt=0)
        elif available == "false":
            avail_filter = Q(count__lte=0)

        if name:
            name_filter = Q(title__icontains=name)
        else:
            name_filter = Q()

        products = products.filter(
            Q(price__gte=min_price),
            Q(price__lte=max_price),
            Q(freeDelivery=strtobool(free_delivery)),
            avail_filter,
            name_filter,
        )

        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(
            {"items": serialized.data, "current_page": current_page, "last_page": 10}
        )


class ProductPopularView(APIView):
    def get(self, request):
        products = Product.objects.annotate(num_reviews=Count("reviews")).order_by(
            "-num_reviews", "-rating"
        )
        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(serialized.data)


class ProductLimitedView(APIView):
    def get(self, request):
        products = Product.objects.filter(Q(count__gt=0), Q(count__lt=4))
        serialized = ProductSerializer(products, many=True)
        # print(json.dumps(serialized.data, ensure_ascii=False))
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(serialized.data)


class BannerView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serialized = ProductSerializer(products, many=True)
        for d in serialized.data:
            d["reviews"] = len(d["reviews"])
        return Response(serialized.data)


class SaleView(APIView):
    def get(self, request):
        current_page = request.GET.get("currentPage")
        products = [product for product in Product.objects.all() if product.sale]
        serialized = SaleSerializer(products, many=True)
        return Response(
            {"items": serialized.data, "current_page": current_page, "last_page": 10}
        )
