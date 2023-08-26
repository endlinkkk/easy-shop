from .models import Category, Subcategory, Image, Product, Tag, Review, Specification, ProductImage
from rest_framework import serializers


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["src", "alt"]


    def get_src(self, obj):
        return obj.src.url

class ImageSerializer(serializers.ModelSerializer):
    # src = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ["src", "alt"]

    # def get_src(self, obj):
    # return obj.src.url


class SubcategoriesSerializer(serializers.ModelSerializer):
    image = ImageSerializer()

    class Meta:
        model = Subcategory
        fields = ("id", "title", "image")


class CategorySerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    subcategories = SubcategoriesSerializer(many=True)

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate", "date"]


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]
