from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

from django.urls import re_path as url
from pwa.views import manifest, service_worker, offline




urlpatterns = [
    path("", views.LandingPage, name="landing"),

    # Auth
    path("login/", views.Login, name="login"),
    path("register/", views.Register, name="register"),
    path("logout/", views.Logout, name="logout"),

    # Dashboard
    path("dashboard/", views.Dashboard, name="dashboard"),

    # Email Verification
    path("verify_email/<str:verification_code>", views.VerifyEmail, name="verify_email"),

    # Profile
    path("user_profile/", views.UserProfile, name="user_profile"),
]