# Generated by Django 4.2.4 on 2023-09-06 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orders", "0008_order_products_alter_order_address_alter_order_city_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("name", models.CharField(max_length=100, null=True)),
                ("month", models.IntegerField(null=True)),
                ("year", models.IntegerField(null=True)),
                ("code", models.IntegerField(null=True)),
                (
                    "order",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.order",
                    ),
                ),
            ],
        ),
    ]
