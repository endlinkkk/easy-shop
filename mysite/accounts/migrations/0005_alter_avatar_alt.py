# Generated by Django 4.2.4 on 2023-08-18 06:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_avatar_src"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="alt",
            field=models.CharField(blank=True, max_length=128, verbose_name="Описание"),
        ),
    ]
