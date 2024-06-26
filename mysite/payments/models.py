from django.db import models
from orders.models import Order


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    card_number = models.IntegerField(null=True)
    month = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    code = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"
