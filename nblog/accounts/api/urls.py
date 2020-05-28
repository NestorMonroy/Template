from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.api import views

urlpatterns = [
    path('hello-view/', views.UserLoginAPIView.as_view()),
]
