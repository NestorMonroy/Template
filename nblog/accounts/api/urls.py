from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from accounts.api import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
