from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    Category,
    Subcategory,
    Image,
    Product,
    Tag,
    Review,
    Specification,
    ProductImage,
    Sale
)

"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['title', 'image']
    list_filter = ['title']
    search_fields = ['title']
    ordering = ['title']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']
    list_filter = ['title']
    search_fields = ['title']
    ordering = ['title']
"""


class CategoryAdminForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)

    class Meta:
        model = Category
        fields = ["title", "image", "image_file", "subcategories"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "image"]
    form = CategoryAdminForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["image_file"]:
            image = Image.objects.create(src=form.cleaned_data["image_file"])
            obj.image = image
        super().save_model(request, obj, form, change)


class SubcategoryAdminForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)

    class Meta:
        model = Subcategory
        fields = ["title", "image", "image_file"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "image"]
    list_filter = ["title"]
    search_fields = ["title"]
    form = SubcategoryAdminForm

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["image_file"]:
            image = Image.objects.create(src=form.cleaned_data["image_file"])
            obj.image = image
        super().save_model(request, obj, form, change)


# -------------------------Product-------------------------------------------------


class ProductAdminForm(forms.ModelForm):
    image_file = forms.ImageField(required=False)
    
    

    #def price(self, obj):
        #return obj.price

    class Meta:
        model = Product
        fields = [
            "title",
            "price",
            "sale",
            "count",
            "rating",
            "category",
            "image_file",
            "tags",
            "date",
            "description",
            "fullDescription",
            "freeDelivery",
            "reviews",
            "specifications",
            "images",
        ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "count", "rating", "category"]
    list_filter = ["title", "price", "count", "rating"]
    search_fields = ["title"]

    form = ProductAdminForm

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.cleaned_data["image_file"]:
            image = ProductImage.objects.create(src=form.cleaned_data["image_file"])
            form.instance.images.add(image)
        elif len(form.instance.images.all()) == 0:
            default_image, created = ProductImage.objects.get_or_create(
                src="products/default.png"
            )
            form.instance.images.add(default_image)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author", "email", "text", "rate"]


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ["name", "value"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["src", "alt"]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    def product_price(self, obj):
        return self.price
    

    product_price.short_description = "Начальная цена продукта ($)" 
    
    
    def add_view(self, request, form_url='', extra_context=None):
        try:
            product_id = int(request.META['HTTP_REFERER'].split('/')[-3])
            self.product = Product.objects.get(id=product_id)
            self.price = self.product.price
        finally:
            return super().add_view(request, form_url, extra_context)

        
    list_display = ["salePrice", "dateFrom", "dateTo"]
    readonly_fields = ['product_price']





    
