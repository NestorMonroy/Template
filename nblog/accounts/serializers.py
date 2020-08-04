from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from dj_rest_auth.serializers import PasswordResetSerializer as RestAuthPasswordChangeSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

User = get_user_model()


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
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.profile.save()
        return user

class PasswordResetSerializer(RestAuthPasswordChangeSerializer):
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


