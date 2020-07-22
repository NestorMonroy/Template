
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.db import models
from django.utils.crypto import get_random_string, salted_hmac
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    """
    This is the user manager for our custom user model. See the User
    model documentation to see what's so special about our user model.
    """

    def create_user(self, email, password=None, is_active=True, is_staff=False, is_superuser=False, str=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)  # change user password
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_superuser
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user


def generate_notifications_token():
    return get_random_string(length=32)


def generate_session_token():
    return get_random_string(length=32)


class SuperuserPermissionSet:
    def __contains__(self, item):
        return True


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, db_index=True, null=True, blank=True,
                              verbose_name=_('E-mail'), max_length=190)
    fullname = models.CharField(max_length=255, blank=True, null=True,
                                verbose_name=_('Nombre'))
    first_name = models.CharField(
        blank=True, null=True, max_length=150, verbose_name='Nombre')
    last_name = models.CharField(
        blank=True, null=True, max_length=150, verbose_name='Apellido')
    username = models.CharField(blank=True, null=True, max_length=100)
    is_active = models.BooleanField(default=True,
                                    verbose_name=_('Is active'))
    is_staff = models.BooleanField(default=False,
                                   verbose_name=_('Is site admin'))
    date_joined = models.DateTimeField(auto_now_add=True,
                                       verbose_name=_('Date joined'))
    locale = models.CharField(max_length=50,
                              #   choices=settings.LANGUAGES,
                              default=settings.LANGUAGE_CODE,
                              verbose_name=_('Language'))
    timezone = models.CharField(max_length=100,
                                default=settings.TIME_ZONE,
                                verbose_name=_('Timezone'))

    require_2fa = models.BooleanField(
        default=False,
        verbose_name=_('Two-factor authentication is required to log in')
    )
    notifications_send = models.BooleanField(
        default=True,
        verbose_name=_('Receive notifications according to my settings below'),
        help_text=_('If turned off, you will not get any notifications.')
    )
    notifications_token = models.CharField(
        max_length=255, default=generate_notifications_token)
    auth_backend = models.CharField(max_length=255, default='native')
    session_token = models.CharField(
        max_length=32, default=generate_session_token)

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._teamcache = {}

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ('email',)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            self.notification_settings.create(
                # action_type='event.order.refund.requested',
                # event=None,
                method='mail',
                enabled=True
            )

    def __str__(self):
        return self.email

    def get_short_name(self) -> str:
        """
        Returns the first of the following user properties that is found to exist:

        * Full name
        * Email address

        Only present for backwards compatibility
        """
        if self.fullname:
            return self.fullname
        else:
            return self.email

    def get_full_name(self) -> str:
        """
        Returns the first of the following user properties that is found to exist:

        * Full name
        * Email address
        """
        if self.fullname:
            return self.fullname
        else:
            return self.email



class ExamplePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text+' - '+self.author.username