from django.urls import path, include, re_path

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from accounts.api import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^profile/$', views.UserDashboardView.as_view(), name='user_profile'),
    path('register/', views.register_view, name='register_view'),



]
