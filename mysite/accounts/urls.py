from django.urls import path
from .views import (
    SignInView,
    SignUpView,
    signOut,
    ProfileView,
    PasswordView,
    AvatarView,
)

urlpatterns = [
    path("sign-in", SignInView.as_view(), name="login"),
    path("sign-up", SignUpView.as_view(), name="register"),
    path("sign-out", signOut),
    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/password", PasswordView.as_view(), name="profile-password"),
    path("profile/avatar", AvatarView.as_view(), name="profile-avatar"),
]
