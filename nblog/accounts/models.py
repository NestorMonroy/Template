from django.db import models
from posts.utils import upload_image_account_path
from django.contrib.auth.models import (
    AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin, BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, full_name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, full_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_account_path,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    confirm = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    # ['full_name'] #python manage.py createsuperuser
    REQUIRED_FIELDS = ['full_name']

    objects = UserProfileManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
