from django.conf.urls import include, url
from django.urls import path, re_path
# from django.contrib.auth.views import LogoutView
# from rest_framework.routers import SimpleRouter
from .views import (social, auth)

# app_name = 'accounts'

# api_router = SimpleRouter()
# api_router.register("users", auth.UserViewSet, basename="users")

urlpatterns = [

    #url(r'^password/reset/$', PasswordResetView.as_view(),
    #     name='rest_password_reset'),
    # url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
    #     name='rest_password_reset_confirm'),
    # url(r'^login/$', LoginView.as_view(), name='rest_login'),
    # # URLs that require a user to be logged in with a valid session / token.
    # url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    # url(r'^user/$', UserDetailsView.as_view(), name='rest_user_details'),
    # url(r'^password/change/$', PasswordChangeView.as_view(),
    #     name='rest_password_change'),

    url(r'^login/$', auth.CreateTokenView.as_view(), name='rest_login'),
    path("registration/", auth.RegistrationView.as_view(), name="rest_register"),

    path('reset-password/', auth.PasswordResetView.as_view(),
         name='reset_password'),
]
