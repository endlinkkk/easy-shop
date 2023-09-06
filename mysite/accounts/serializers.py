from rest_framework import serializers
from .models import Avatar, Profile
from django.contrib.auth.models import User


class AvatarSerializer(serializers.ModelSerializer):
    # src = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    # def get_src(self, obj):
    # return obj.src.url


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer()

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]



class SignUpSerializer(serializers.Serializer):
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Name should be at least 3 characters long.')
        return value

    def validate_username(self, value):
        # Проверка на уникальность имени пользователя
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password should be at least 8 characters long.')
        return value