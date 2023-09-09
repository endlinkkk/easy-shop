# Generated by Django 4.2.4 on 2023-09-07 17:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0022_alter_product_count_alter_product_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="date",
            field=models.CharField(
                blank=True, default=datetime.date(2023, 9, 7), max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.CharField(
                blank=True, default=datetime.date(2023, 9, 7), max_length=100, null=True
            ),
        ),
    ]
