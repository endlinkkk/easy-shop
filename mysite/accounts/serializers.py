from rest_framework import serializers
from .models import Avatar, Profile

class AvatarSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField() 

    class Meta:
        model = Avatar
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url
    
class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(read_only=True) 

    class Meta:
        model = Profile
        fields = ["fullName", "email", "phone", "avatar"]