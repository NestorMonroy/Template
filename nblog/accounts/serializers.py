from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from allauth.account.views import ConfirmEmailView as AllAuthVerifyEmailView

from rest_framework import serializers
from dj_rest_auth.serializers import (
    LoginSerializer as RestAuthLoginSerializer,
    PasswordChangeSerializer as RestAuthPasswordChangeSerializer,
    PasswordResetSerializer as RestAuthPasswordResetSerializer,
    PasswordResetConfirmSerializer as RestAuthPasswordResetConfirmSerializer,
)
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import (email_address_exists,
                           get_username_max_length)
from allauth.account.utils import setup_user_email

from dj_rest_auth.models import TokenModel

from rest_framework.settings import api_settings as drf_settings
from .models import ExamplePost
from .mixins import ErrorsSerializerMixin

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = User
        fields = ('id', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6, 'required': True}
        }

    def create(self, valid_data):
        """Create a new user with encrypt password and return user"""
        user = User.objects.create_user(**valid_data)
        return user

    def update(self, instance, valid_data):
        """Update a user and password, and return it"""
        password = valid_data.pop('password', None)
        user = super().update(instance, valid_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate user credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class PostSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        queryset=User.objects.filter(), slug_field='username'
    )

    class Meta:
        model = ExamplePost
        fields = ('id', 'author', 'text', 'created', 'updated')


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def update(self, instance, valid_data):
        """Update a user and password, and return it"""
        password = valid_data.pop('password', None)
        user = super().update(instance, valid_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def create(self, valid_data):
        """Create a new user with encrypt password and return user"""
        return get_user_model().objects.create_user(**valid_data)


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=100, required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6}
        }

    def update(self, instance, valid_data):
        """Update a user and password, and return it"""
        password = valid_data.pop('password', None)
        user = super().update(instance, valid_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def create(self, valid_data):
        print(self.user)
        """Create a new user with encrypt password and return user"""
        return User().objects.create_user(**valid_data)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class UserSerializerLite(serializers.ModelSerializer):
    """
    A lightweight read-only serializer used for passing the bare minimum amount
    of information about a user to the client; currently only used for login errors
    in-case the client needs that information to submit a POST (for example, to resend
    the verification email, and for the RegisterView)
    """

    class Meta:
        model = User
        fields = ("email", "name", "change_password")
        read_only_fields = ("email", "name", "change_password")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        """
        Does the usual login validation, but as w/ LoginForm it adds some explicit checks for astrosat_users-specific stuff
        (this is the right place to put it; the KnoxLoginView has its own KnoxTokenSerializer for users _and_ tokens,
        but it uses this serializer for the user and so validation will be checked when processing the view.)
        """

        instance = super().validate(attrs)

        user = instance["user"]
        user_serializer = UserSerializerLite(user)

        adapter = get_adapter(self.context.get("request"))
        try:
            adapter.check_user(user)
        except Exception as e:
            msg = {
                "user": user_serializer.data,
                drf_settings.NON_FIELD_ERRORS_KEY: str(e),
            }
            raise ValidationError(msg)

        return instance
        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs
# class LoginSerializer(ErrorsSerializerMixin, RestAuthLoginSerializer):

#     # just a bit more security...
#     password = serializers.CharField(
#         write_only=True, style={"input_type": "password"})

#     # some extra fields...
#     id = serializers.UUIDField(read_only=True, source="uuid")
#     is_verified = serializers.BooleanField(read_only=True)
#     is_approved = serializers.BooleanField(read_only=True)
#     accepted_terms = serializers.BooleanField(read_only=True)
#     change_password = serializers.BooleanField(read_only=True)

#     # (even though I don't need the 'username' field, the 'validate()' fn checks its value)
#     # (so I haven't bothered removing it; the client can deal w/ this)

#     def validate(self, attrs):
#         """
#         Does the usual login validation, but as w/ LoginForm it adds some explicit checks for astrosat_users-specific stuff
#         (this is the right place to put it; the KnoxLoginView has its own KnoxTokenSerializer for users _and_ tokens,
#         but it uses this serializer for the user and so validation will be checked when processing the view.)
#         """

#         instance = super().validate(attrs)

#         user = instance["user"]
#         user_serializer = UserSerializerLite(user)

#         adapter = get_adapter(self.context.get("request"))
#         try:
#             adapter.check_user(user)
#         except Exception as e:
#             msg = {
#                 "user": user_serializer.data,
#                 drf_settings.NON_FIELD_ERRORS_KEY: str(e),
#             }
#             raise ValidationError(msg)

#         return instance


class VerifyEmailSerializer(ErrorsSerializerMixin, serializers.Serializer):

    key = serializers.CharField()

    def validate(self, data):

        try:
            view = AllAuthVerifyEmailView()
            view.kwargs = (
                data
            )  # little hack here b/c I'm using a view outside a request
            emailconfirmation = view.get_object()
            data["confirmation"] = emailconfirmation
        except Exception:
            raise serializers.ValidationError("This is an invalid key.")

        return data


class SendEmailVerificationSerializer(ErrorsSerializerMixin, serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, data):

        email_data = data["email"]
        try:
            user = User.objects.get(email=email_data)
            data["user"] = user
        except User.DoesNotExist:
            raise serializers.ValidationError(
                f"Unable to find user with '{email_data}' address."
            )

        return data


# class TokenSerializer(serializers.Serializer):
#     user = LoginSerializer()
#     token = serializers.SerializerMethodField()


#     # TODO: DO _REAL_ VALIDATION ON THE TOKEN


class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = TokenModel
        fields = ('key',)

    def get_token(self, obj):
        instance, token = obj["token"]
        return token
