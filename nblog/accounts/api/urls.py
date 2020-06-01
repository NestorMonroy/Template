from django.urls import path, include, re_path

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^register/$', views.RegisterView.as_view(), name='user_create'),
    url(r'^profile/(?P<pk>[0-9]+)/$',
        views.ProfileDetailView.as_view(), name='user_detail'),
    url(r'^logout$', views.logoutHandler, name='logout'),
]
