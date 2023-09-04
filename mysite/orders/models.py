from django.db import models
from catalog.models import Product
from django.contrib.auth.models import User

# TODO
# Сделать basket
# СДелать order




# Когда пользователь нажимает добавить товар в корзину мы создаем BasketItem и добавляем его в корзину

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    
class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)