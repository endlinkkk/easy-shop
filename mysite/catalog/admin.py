from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Subcategory, Image, Product, Tag, Review, Specification, ProductImage

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

    class Meta:
        model = Product
        fields = ["title", "price", "count", "rating", "category", "image_file", "tags", "date", "description", "fullDescription", "freeDelivery", "reviews", "specifications", "images"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "count", "rating", "category"]
    list_filter = ["title", "price", "count", "rating"]
    search_fields = ["title"]

    form = ProductAdminForm
    
    '''
    def save_model(self, request, obj, form, change):
        """Создает объект из загруженной фотки, но не прикрепляет его к продукту"""
        super().save_model(request, obj, form, change)  # Сначала сохраняем объект Product
        p = Product.objects.get(id=obj.id)
        if form.cleaned_data["image_file"]:
            image = ProductImage.objects.create(src=form.cleaned_data["image_file"])
            image.save()
            print(f"Создали и сохранили кастомную картинку {image}")
            p.images.add(image)  # Добавляем созданный объект ProductImage к полю "images" объекта Product
            print(f'Добавили к продукту картинку {p}')
        elif len(p.images.all()) == 0:
            default_image = ProductImage.objects.create()
            default_image.save()
            print(f"Создали и сохранили стандартную картинку {default_image}")
            p.images.add(default_image)
            print(f'Добавили к продукту картинку {p}')
    '''
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Сначала сохраняем объект Product
        if form.cleaned_data["image_file"]:
            print(form.cleaned_data["image_file"])
            image = ProductImage.objects.create(src=form.cleaned_data["image_file"])
            image.save()
            print(f"Создали и сохранили кастомную картинку {image}")
            obj.images.add(image)  # Добавляем созданный объект ProductImage к полю "images" объекта Product
            print(f"Сохранили и добавили картинку, но картинка не привязана к продукту")
        elif len(obj.images.all()) == 0:
            default_image = ProductImage.objects.create()
            default_image.save()
            print(f"Создали и сохранили картинку {default_image}")
            obj.images.add(default_image)
            print(f'Добавили к продукту картинку {obj}')
            print(f"Сохранили и добавили дефолтную картинку, но картинка не привязана к продукту")

            
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