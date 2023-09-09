from django.db import models
from catalog.models import Product
from django.utils import timezone
from django.contrib.auth.models import User


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.id}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product} - {self.quantity}"


# -------------старый ордер

# class Order(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     createdAt = models.DateField(verbose_name="Дата создания", default=timezone.now)
#     fullName = models.CharField(max_length=100)
#     email = models.EmailField(max_length=254, null=True)
#     phone = models.PositiveIntegerField(
#         blank=True, null=True, unique=True, verbose_name="Номер телефона"
#     )
#     deliveryType = models.CharField(max_length=10)
#     paymentType = models.CharField(max_length=20)
#     totalCost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
#     status = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     address = models.CharField(max_length=100)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdAt = models.DateField(verbose_name="Дата создания", default=timezone.now)
    fullName = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True)
    phone = models.CharField(
        blank=True, null=True, unique=True, verbose_name="Номер телефона", max_length=12
    )
    deliveryType = models.CharField(max_length=10, null=True)
    paymentType = models.CharField(max_length=20, null=True)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=100, null=True)
    products = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"{self.id} - {self.createdAt} - {self.status}"
