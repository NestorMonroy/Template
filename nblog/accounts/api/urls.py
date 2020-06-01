from django.urls import path, include, re_path

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from accounts.api import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^profile/$', views.UserDashboardView.as_view(), name='user_profile'),
    url(r'^register/step-1$', views.step1Handler, name='register-step-1'),
    url(r'^register/step-2$', views.step2Handler, name='register-step-2'),
    url(r'^register$', views.registerHandler, name='register'),
    url(r'^activate/(?P<token>.+)$', views.activeAccountHandler, name='activate'),
    url(r'^logout$', views.logoutHandler, name='logout'),
    url(r'^reset_password/(?P<token>.+)$',
        views.resetPasswordHandler, name='reset-password'),
    url(r'^reset_password$', views.resetPasswordFormHandler,
        name='reset-password-form'),


]
