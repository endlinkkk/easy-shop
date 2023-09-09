from django.contrib import admin
from .models import Basket, BasketItem, Order

# Register your models here.


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    pass


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderItemAdmin(admin.ModelAdmin):
    pass
