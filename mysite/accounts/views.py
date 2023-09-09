from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Profile, Avatar
from .serializers import ProfileSerializer, SignUpSerializer

import json

# Create your views here.


class SignInView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        user_data = json.loads(request.body)
        print(user_data)
        serializer = SignUpSerializer(data=user_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")
        if serializer.is_valid():
            try:
                print("try")
                user = User.objects.create_user(username=username, password=password)
                avatar, created = Avatar.objects.get_or_create(
                    src="avatars/default.png"
                )
                profile = Profile.objects.create(
                    user=user, fullName=name, avatar=avatar
                )
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)

                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("поймали на ошибке")
            return Response(serializer.errors, status=400)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        print(request.data)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        user = User.objects.get(username=request.user)
        user.set_password(request.data["newPassword"])
        print(request.data)
        user.save()
        return Response(status=status.HTTP_200_OK)


class AvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        avatar = Avatar()
        avatar.src = request.FILES["avatar"]
        avatar.save()
        profile = Profile.objects.get(user=request.user)
        profile.avatar = avatar
        profile.save()
        return Response(status=status.HTTP_200_OK)
