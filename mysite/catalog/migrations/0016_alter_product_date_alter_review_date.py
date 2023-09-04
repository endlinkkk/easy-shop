# Generated by Django 4.2.4 on 2023-08-28 08:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0015_alter_product_date_alter_review_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="date",
            field=models.CharField(
                blank=True, default=datetime.date(2023, 8, 28), max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.CharField(
                blank=True,
                default=datetime.date(2023, 8, 28),
                max_length=100,
                null=True,
            ),
        ),
    ]