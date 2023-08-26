# Generated by Django 4.2.4 on 2023-08-20 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
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
                        default="category/default.png",
                        upload_to="category/pictures/",
                        verbose_name="Ссылка",
                    ),
                ),
                (
                    "alt",
                    models.CharField(
                        default="Описание картинки",
                        max_length=128,
                        verbose_name="Описание",
                    ),
                ),
            ],
            options={
                "verbose_name": "Изображение категории",
                "verbose_name_plural": "Изображения категории",
            },
        ),
        migrations.CreateModel(
            name="SubImage",
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
                        default="subcategory/default.png",
                        upload_to="subcategory/pictures/",
                        verbose_name="Ссылка",
                    ),
                ),
                (
                    "alt",
                    models.CharField(
                        default="Описание картинки",
                        max_length=128,
                        verbose_name="Описание",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Subcategory",
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
                ("title", models.CharField(max_length=100)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.subimage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("title", models.CharField(max_length=100)),
                (
                    "image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="catalog.image"
                    ),
                ),
                (
                    "subcategories",
                    models.ManyToManyField(
                        related_name="category", to="catalog.subcategory"
                    ),
                ),
            ],
        ),
    ]
