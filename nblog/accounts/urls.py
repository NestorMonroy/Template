from django.conf.urls import include, url
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from rest_framework.routers import SimpleRouter
from .views import (social, auth)

app_name = 'accounts'


api_router = SimpleRouter()
api_router.register("users", auth.UserViewSet, basename="users")

urlpatterns = [
    path("", include(api_router.urls)),
    # path(
    #     "customers/<slug:customer_id>/", CustomerDetailView.as_view(), name="customers-detail"
    # ),
    # path(
    #     "customers/<slug:customer_id>/users/",
    #     CustomerUserListView.as_view(),
    #     name="customer-users-list",
    # ),
    # path(
    #     "customers/<slug:customer_id>/users/<slug:user_id>/",
    #     CustomerUserDetailView.as_view(),
    #     name="customer-users-detail",
    # ),
    # # overwrite the rest_auth.urls to cope w/ the idiosyncracies of astrosat_users
    # # (and to exclude the built-in user ViewSets)
    # # path("authentication/", include("dj_rest_auth.urls")),
    # # path("authentication/registration/", include("dj_rest_auth.registration.urls")),
    # path("authentication/login/", LoginView.as_view(), name="rest_login"),
    # path("authentication/logout/", LogoutView.as_view(), name="rest_logout"),
    # path(
    #     "authentication/password/change/",
    #     PasswordChangeView.as_view(),
    #     name="rest_password_change",
    # ),
    # path(
    #     "authentication/password/reset/",
    #     PasswordResetView.as_view(),
    #     name="rest_password_reset",
    # ),
    # path(
    #     "authentication/password/verify-reset/",
    #     PasswordResetConfirmView.as_view(),
    #     name="rest_password_reset_confirm",
    # ),
    # a "special" api_urlpattern that authenticates using django-allauth NOT django-rest-auth
    path("authentication/registration/", auth.RegisterView.as_view(), name="rest_register"),
    path(
        "authentication/registration/verify-email/",
        auth.VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    path(
        "authentication/send-email-verification/",
        auth.SendEmailVerificationView.as_view(),
        name="rest_send_email_verification",
    ),
    path("token", auth.CreateTokenView.as_view(), name="token"),
]

# urlpatterns = [
#     path('login/', auth.LoginView.as_view(), name='login'),

#     path('create/', auth.CreateUserView.as_view(), name='create'),
#     path('token/', auth.CreateTokenView.as_view(), name='token'),
#     path('me/', auth.UserViewSet.as_view(), name='me'),
#     path('register/', auth.RegisterView.as_view(), name='register'),
#     url(r'^logout/$', LogoutView.as_view(), name='logout'),
#     # path('register/', auth.RegistrationAPIView.as_view(),name='register'),

# ]
