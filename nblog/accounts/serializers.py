from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings as drf_settings
from dj_rest_auth.serializers import (
    PasswordResetSerializer as ChangePasswordResetSerializer,
    LoginSerializer as ChangeLoginSerializer

)
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth import authenticate


User = get_user_model()

from rest_framework.authtoken.models import Token

class UserSerializerLite(serializers.ModelSerializer):
    """
    A lightweight read-only serializer used for passing the bare minimum amount
    of information about a user to the client; currently only used for login errors
    in-case the client needs that information to submit a POST (for example, to resend
    the verification email, and for the RegisterView)
    """

    class Meta:
        model = User
        fields = ("email",)
        read_only_fields = ("email",)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'},trim_whitespace=False)

    # def _validate_email(self, email, password):
    #     user = None

    #     if email and password:
    #         user = self.authenticate(email=email, password=password)
    #     else:
    #         msg = _('Must include "email" and "password".')
    #         raise exceptions.ValidationError(msg)
    #     print(user)

    #     return user

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate user credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        read_only_fields = ("email",)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

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

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password1', ''),

        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.profile.save()
        return user

        opts = {
            'domain_override': getattr(settings, 'FRONT_URL'),
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

class PasswordResetSerializer(ChangePasswordResetSerializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        ###### FILTER YOUR USER MODEL ######
        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'domain_override': getattr(settings, 'FRONT_URL'),
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        opts.update(self.get_email_options())
        self.reset_form.save(**opts)



class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=False, allow_blank=True)
    # just a bit more security...
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    is_verified = serializers.BooleanField(read_only=True)



    
    # some extra fields...
    # id = serializers.UUIDField(read_only=True, source="uuid")
    # is_verified = serializers.BooleanField(read_only=True)
    # is_approved = serializers.BooleanField(read_only=True)
    # accepted_terms = serializers.BooleanField(read_only=True)
    # change_password = serializers.BooleanField(read_only=True)

    # (even though I don't need the 'username' field, the 'validate()' fn checks its value)
    # (so I haven't bothered removing it; the client can deal w/ this)

    def validate(self, attrs):
        """
        Does the usual login validation, but as w/ LoginForm it adds some explicit checks for astrosat_users-specific stuff
        (this is the right place to put it; the KnoxLoginView has its own Token for users _and_ tokens,
        but it uses this serializer for the user and so validation will be checked when processing the view.)
        """

        instance = super().validate(attrs)

        email = instance["email"]
        user_serializer = UserSerializerLite(email)

        adapter = get_adapter(self.context.get("request"))


        return instance

