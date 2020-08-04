from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from dj_rest_auth.views import LoginView, PasswordResetView
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth.forms import PasswordResetForm
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from ..serializers import (
    UserDetailsSerializer,
    PasswordResetSerializer,
    RegisterSerializer
)
from dj_rest_auth.models import TokenModel



sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)
class RegistrationView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny, ]
    token_model = TokenModel

    swagger_tags = ["User"]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={201: "Verification e-mail sent."},
    )

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegistrationView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

            return TokenSerializer(user.auth_token, context=self.get_serializer_context()).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if allauth_settings.EMAIL_VERIFICATION != \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            if getattr(settings, 'REST_USE_JWT', False):
                self.access_token, self.refresh_token = jwt_encode(user)
            else:
                create_token(self.token_model, user, serializer)

        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return user

    
    def post(self, *args, **kwargs):
        """Register new user

        Use this endpoint to register a new user using a username/email and password
        """
        return super().post(*args, **kwargs)


class PasswordResetView(generics.GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)
    
    swagger_tags = ["User"]

    @swagger_auto_schema(
        responses={200: "Password reset e-mail has been sent."},
        request_body=PasswordResetView,
    )

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )

