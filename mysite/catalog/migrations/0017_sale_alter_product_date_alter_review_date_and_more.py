# Generated by Django 4.2.4 on 2023-08-29 13:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0016_alter_product_date_alter_review_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("salePrice", models.DecimalField(decimal_places=2, max_digits=10)),
                ("dateFrom", models.DateField()),
                ("dateTo", models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name="product",
            name="date",
            field=models.CharField(
                blank=True, default=datetime.date(2023, 8, 29), max_length=100
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.CharField(
                blank=True,
                default=datetime.date(2023, 8, 29),
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="sale",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.sale",
            ),
        ),
    ]
