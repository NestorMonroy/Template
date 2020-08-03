from django.conf.urls import include, url
from django.urls import path, re_path
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth.views import LogoutView

from .views import (social, auth)

app_name = 'accounts'

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),

    path('create/', auth.CreateUserView.as_view(), name='create'),
    path('token/', auth.CreateTokenView.as_view(), name='token'),
    path('me/', auth.UserViewSet.as_view(), name='me'),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('registration/', RegisterView.as_view(), name='account_signup'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # path('register/', auth.RegistrationAPIView.as_view(),name='register'),

]
