# Generated by Django 4.2.4 on 2023-08-23 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0009_alter_subcategory_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImage",
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
                (
                    "src",
                    models.ImageField(
                        default="products/default.png",
                        upload_to="products/pictures/",
                        verbose_name="Ссылка",
                    ),
                ),
                (
                    "alt",
                    models.CharField(
                        default="Описание картинки",
                        max_length=128,
                        null=True,
                        verbose_name="Описание",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
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
                ("author", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, verbose_name="Почта")),
                ("text", models.TextField()),
                ("rate", models.IntegerField(verbose_name="Оценка")),
            ],
        ),
        migrations.CreateModel(
            name="Specification",
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
                ("name", models.CharField(max_length=50)),
                ("value", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("count", models.IntegerField()),
                ("date", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField()),
                ("fullDescription", models.TextField()),
                ("freeDelivery", models.BooleanField(default=False)),
                ("rating", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="catalog.category",
                    ),
                ),
                (
                    "images",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productimage",
                    ),
                ),
                (
                    "reviews",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.review",
                    ),
                ),
                (
                    "specifications",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.specification",
                    ),
                ),
                (
                    "tags",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="catalog.tag",
                    ),
                ),
            ],
        ),
    ]
