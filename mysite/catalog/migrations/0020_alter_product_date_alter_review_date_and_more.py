# Generated by Django 4.2.4 on 2023-09-03 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0019_remove_sale_product_product_sale"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="date",
            field=models.CharField(
                blank=True, default=datetime.date(2023, 9, 3), max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.CharField(
                blank=True, default=datetime.date(2023, 9, 3), max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="sale",
            name="dateFrom",
            field=models.DateField(verbose_name="Начало скидки"),
        ),
        migrations.AlterField(
            model_name="sale",
            name="dateTo",
            field=models.DateField(verbose_name="Конец скидки"),
        ),
        migrations.AlterField(
            model_name="sale",
            name="salePrice",
            field=models.IntegerField(verbose_name="Процент скидки %"),
        ),
    ]
