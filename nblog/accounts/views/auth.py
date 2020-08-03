from collections import OrderedDict

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.translation import gettext_lazy as _
from rest_framework import views, viewsets, mixins, status
from rest_framework import status, generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import complete_signup, send_email_confirmation
from allauth.exceptions import ImmediateHttpResponse

from dj_rest_auth.views import (
    LoginView as RestAuthLoginView,
    LogoutView as RestAuthLogoutView,
    PasswordChangeView as RestAuthPasswordChangeView,
    PasswordResetView as RestAuthPasswordResetView,
    PasswordResetConfirmView as RestAuthPasswordResetConfirmView,
)
from dj_rest_auth.registration.views import (
    RegisterView as RestAuthRegisterView,
    VerifyEmailView as RestAuthVerifyEmailView,
)

# from astrosat_users.conf import app_settings as astrosat_users_settings
from ..serializers import (
    UserSerializerLite,
    TokenSerializer,
    VerifyEmailSerializer,
    SendEmailVerificationSerializer,
    UserSerializer,
    RegistrationSerializer,
    AuthTokenSerializer,
    RestAuthLoginSerializer


)
from ..utils import create_knox_token

User = get_user_model()

REGISTRATION_CLOSED_MSG = _("We are sorry, but the sign up is currently closed.")


###############
# permissions #
###############


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # anybody can do GET, HEAD, or OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # only an unauthenticated user can do POST, PUT, PATCH, DELETE
        user = request.user
        return not user.is_authenticated


# class AllowRegistrationPermission(BasePermission):
#     def has_permission(self, request, view):
#         if not astrosat_users_settings.ASTROSAT_USERS_ALLOW_REGISTRATION:
#             # raising an error instead of returning False in order to get a custom message
#             # as per https://github.com/encode/django-rest-framework/issues/3754#issuecomment-206953020
#             raise PermissionDenied(REGISTRATION_CLOSED_MSG)
#         return True


#################
# swagger stuff #
#################


# b/c ACCOUNT_USERNAME_REQURED is False and ACCOUNT_EMAIL_REQUIRED is True, not all fields
# from the LoginSerializer/RegisterSerializer are used in the LoginView/RegisterView
# therefore, I overide the swagger documentation w/ the following schemas...

_login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=OrderedDict(
        (
            # ("username", openapi.Schema(type=openapi.TYPE_STRING, example="admin")),
            (
                "email",
                openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    example="nestor@gmail.com",
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
            # ("username", openapi.Schema(type=openapi.TYPE_STRING, example="admin")),
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


#########
# views #
#########


@method_decorator(
    swagger_auto_schema(
        request_body=_login_schema, responses={status.HTTP_200_OK: TokenSerializer}
    ),
    name="post",
)
@method_decorator(sensitive_post_parameters("password"), name="dispatch")
class LoginView(RestAuthLoginView):
    """
    Just like rest_auth.LoginView but removes all of the JWT logic
    (no need to override login/save - that is all done in the serializer)
    """

    permission_classes = [IsNotAuthenticated]

    def get_response(self):
        # note that this uses the KnoxTokenSerializer
        # which has custom token validation
        # which includes the LoginSerializer
        # which adds extra astrosat_users validation
        serializer_class = self.get_response_serializer()

        data = {"username": self.user, "token": self.token}
        serializer = serializer_class(instance=data, context={"request": self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(RestAuthLogoutView):
    """
    Just like rest_auth.LogoutView but deletes knox token
    prior to passing to logout
    """

    permission_classes = [IsAuthenticated]

    def logout(self, request):
        token = request.auth
        if token:
            token.delete()
        return super().logout(request)


class PasswordChangeView(RestAuthPasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.
    """

    pass


class PasswordResetView(RestAuthPasswordResetView):
    """
    Calls Django Auth PasswordResetForm save method.
    """

    pass


class PasswordResetConfirmView(RestAuthPasswordResetConfirmView):
    """
    This is the endpoint that the client POSTS to after having recieved
    the "rest_confirm_password" view.
    Takes the following parameters:
    ```
    {
        "key": "string",
        "uid": "string"
    }
    ```
    """

    pass


@method_decorator(sensitive_post_parameters("password1", "password2"), name="dispatch")
@method_decorator(
    swagger_auto_schema(
        request_body=_register_schema,
        responses={status.HTTP_200_OK: UserSerializerLite},
    ),
    name="post",
)
class RegisterView(RestAuthRegisterView):

    permission_classes = [IsNotAuthenticated,]

    def get_response_data(self, user):
        # just return a lightweight representation of the user
        # no need to get private details or tokens at this point
        serializer = UserSerializerLite(instance=user)
        return serializer.data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        complete_signup(
            self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None
        )
        return user


class VerifyEmailView(RestAuthVerifyEmailView):
    """
    This is the endpoint that the client POSTS to after having recieved
    the "account_confirm_email" view.
    takes the following parameters:
    ```
    {
        "key": "string"
    }
    ```
    """

    def get_serializer(self, *args, **kwargs):
        # NOTE THAT dj-rest-auth DOESN'T SUPPORT OVERWRITING THIS SERIALIZER, SO I HARD-CODE IT HERE
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        confirmation = serializer.validated_data["confirmation"]
        confirmation.confirm(self.request)

        return Response({"detail": _("ok")}, status=status.HTTP_200_OK)


class SendEmailVerificationView(GenericAPIView):
    """
    An endpoint which re-sends the confirmation email to the
    provided email address (no longer doing it automatically
    upon a failed login)
    """

    serializer_class = SendEmailVerificationSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        if not user.is_verified:
            send_email_confirmation(request, user)
            msg = _("Verification email sent.")
        else:
            msg = _(f"No verification email sent; {user} is already verified.")

        return Response({"detail": msg})


#

class PostViewSet(viewsets.ModelViewSet):
    """Manage the post in the database"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class UserViewSet(RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer


class RegistrationAPIView(APIView):
    
    def post(self, request):
        print(self, "nestor")
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("#Incoming Request#\nType: Register\nUser: "+str(user.id)+"\n#End Request")
            return Response({'token': Token.objects.get(user=user).key,"userEmail":user.email,"userId":user.id},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES