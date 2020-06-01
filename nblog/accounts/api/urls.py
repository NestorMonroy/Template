from django.urls import path, include, re_path

from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from accounts.api import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='user_login'),
    url(r'^profile/$', views.UserDashboardView.as_view(), name='user_profile'),
#     path('register/', views.register_view, name='register_view'),
    url(r'^register/step-1$', views.step1Handler, name='register-step-1'),
    url(r'^register/step-2$', views.step2Handler, name='register-step-2'),
    url(r'^register$', views.registerHandler, name='register'),



#     path('password-reset/', auth_views.PasswordResetView.as_view(
#             template_name='registration/password_reset_form.html'), name='password_reset'),
#     path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
#             auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')


]
