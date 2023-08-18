from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_desplay = ['fullName', 'phone', 'email', 'balance', 'avatar']
    list_filter = ['fullName', 'balance']
    search_fields = ['fullName', 'phone']
    ordering = ['fullName', 'balance']

# Register your models here.

