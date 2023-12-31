# Generated by Django 4.2.4 on 2023-08-21 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_alter_category_subcategories_alter_subimage_alt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.image",
            ),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="image",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.subimage",
            ),
        ),
    ]
