from django.contrib import admin
from .models import Profile, Avatar


@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_desplay = ["fullName", "phone", "email", "balance", "avatar"]
    list_filter = ["fullName", "balance"]
    search_fields = ["fullName", "phone"]
    ordering = ["fullName", "balance"]


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    pass


# Register your models here.
