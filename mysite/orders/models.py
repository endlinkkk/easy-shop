from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User



class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    
class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} - {self.quantity}"