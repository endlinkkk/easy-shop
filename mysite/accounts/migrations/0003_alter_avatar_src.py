# Generated by Django 4.2.4 on 2023-08-18 05:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_profile_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="src",
            field=models.ImageField(
                default="default.png", upload_to="user_avatars/", verbose_name="Ссылка"
            ),
        ),
    ]
