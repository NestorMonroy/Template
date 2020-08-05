from collections import OrderedDict
from django.contrib.auth import login as django_login
from django.utils.translation import ugettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from dj_rest_auth.views import (
    LoginView as ChangeLoginView,
    PasswordResetView  )
from dj_rest_auth.registration.views import RegisterView
from django.contrib.auth.forms import PasswordResetForm
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from ..serializers import (
    UserDetailsSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    AuthTokenSerializer,
    UserSerializerLite,
)
from django.conf import settings
from rest_framework.authtoken.models import Token
from ..utils import create_token
from rest_framework.settings import api_settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.views import ObtainAuthToken

User = get_user_model()

# sensitive_post_parameters_n = method_decorator(
#     sensitive_post_parameters(
#         'password', 'old_password', 'new_password1', 'new_password2'
#     )
# )

_login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=OrderedDict(
        (
            (
                "email",
                openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    example="nestor@blog.com",
                ),
            ),
            ("password", openapi.Schema(type=openapi.TYPE_STRING, example="password")),
        )
    ),
)


_register_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=OrderedDict(
        (
            (
                "email",
                openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            ),
            (
                "password1",
                openapi.Schema(type=openapi.TYPE_STRING, example="superpassword23"),
            ),
            (
                "password2",
                openapi.Schema(type=openapi.TYPE_STRING, example="superpassword23"),
            ),
            ("accepted_terms", openapi.Schema(type=openapi.TYPE_BOOLEAN)),
        )
    ),
)

@method_decorator(
    swagger_auto_schema(
        request_body=_login_schema, responses={status.HTTP_200_OK: AuthTokenSerializer}
    ),
    name="post",
)
@method_decorator(sensitive_post_parameters("password"), name="dispatch")
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@method_decorator(
    swagger_auto_schema(
        request_body=_register_schema,
        responses={status.HTTP_200_OK: UserSerializerLite},
    ),
    name="post",
)
@method_decorator(sensitive_post_parameters("password1", "password2"), name="dispatch")
class RegistrationView(RegisterView):
    serializer_class = RegisterSerializer

    def get_response_data(self, user):
        print(user)
        # just return a lightweight representation of the user
        # no need to get private details or tokens at this point
        serializer = UserSerializerLite(instance=user)
        return serializer.data

class PasswordResetView(generics.GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)
    

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