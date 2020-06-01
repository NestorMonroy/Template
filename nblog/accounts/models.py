from django.db import models
from posts.utils import upload_image_account_path
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.utils import timezone
from django.core.mail import send_mail

import datetime
import os
import uuid

from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .validators import UnicodeUsernameValidator

from .managers import UserProfileManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    timestamp = models.DateTimeField(auto_now_add=True)
    # confirm     = models.BooleanField(default=False)
    # confirmed_date     = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    # REQUIRED_FIELDS = []  # ['full_name'] #python manage.py createsuperuser

    objects = UserProfileManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=240, blank=True)
    city = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    active = models.BooleanField(default=False)

    @property
    def is_active(self):
        return self.active

    def save(self, *args, **kwargs):
        try:
            existing = Profile.objects.all().get(user=self.user)
            self.id = existing.id
        except Profile.DoesNotExist:
            pass
        # if self.tab < 0:
        # 	self.tab = 0
        models.Model.save(self, *args, **kwargs)

    @classmethod
    def new(cls, email, password, full_name,):
        user = User.objects.create_user(email, password, full_name)
        user.full_name = full_name
        user.save()
        print('Your username is  {user}')    
        profile = Profile(user=user, active=False)
        profile.save()
        return user


class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status_content = models.CharField(max_length=240)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "statuses"

    def __str__(self):
        return str(self.user_profile)


class AccountActivationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.username


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.username

    @classmethod
    def new(cls, user):
        prt = cls(user=user, token=uuid.uuid4())
        prt.save()
        return prt
