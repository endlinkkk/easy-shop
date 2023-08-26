from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Product, Review, Tag
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, TagSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import date
import json


# Create your views here.
class CategoriesView(APIView):
    def get(self, request):
        print("Work CategoriesView")
        categories = Category.objects.all()
        # print("cat", categories)
        serialized = CategorySerializer(categories, many=True)
        # print(json.dumps(serialized.data, ensure_ascii=False))
        return Response(serialized.data)


class ProductIdView(APIView):
    def get(self, request, id):
        print("Work ProductIdView", id)
        # data = json.loads(request.body)
        product = get_object_or_404(Product, pk=id)
        print(product.images.all())
        serialized = ProductSerializer(product)
        print(json.dumps(serialized.data, ensure_ascii=False))
        return Response(serialized.data)


class ProductIdReviewView(APIView):
    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        data = request.data
        print(data)
        review = Review.objects.create(author=data['author'], email=data['email'], text=data['text'], rate=data['rate'], date=date.today())
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
        print('work catalog')
        name = request.GET.get('filter[name]', '')  # Получение значения параметра filter[name]
        min_price = request.GET.get('filter[minPrice]', '0')  # Получение значения параметра filter[minPrice]
        max_price = request.GET.get('filter[maxPrice]', '50000')  # Получение значения параметра filter[maxPrice]
        free_delivery = request.GET.get('filter[freeDelivery]', 'false')  # Получение значения параметра filter[freeDelivery]
        available = request.GET.get('filter[available]', 'false')  # Получение значения параметра filter[available]
        current_page = request.GET.get('currentPage', '1')  # Получение значения параметра currentPage
        sort = request.GET.get('sort', 'price')  # Получение значения параметра sort
        sort_type = request.GET.get('sortType', 'inc')  # Получение значения параметра sortType
        limit = request.GET.get('limit', '20') 
        print(name, max_price, min_price)
        products = Product.objects