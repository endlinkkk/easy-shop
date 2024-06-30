from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
