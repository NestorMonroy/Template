from django.conf.urls import include, url
from django.urls import path, re_path
# from django.contrib.auth.views import LogoutView
# from rest_framework.routers import SimpleRouter
from .views import (social, auth)

# app_name = 'accounts'

# api_router = SimpleRouter()
# api_router.register("users", auth.UserViewSet, basename="users")

urlpatterns = [
    path('reset-password/', auth.PasswordResetView.as_view(),
         name='reset-password'),
]
