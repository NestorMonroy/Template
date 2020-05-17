from django.db import models
from posts.utils import upload_image_account_path
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
# Create your models here.


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_account_path,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # confirm     = models.BooleanField(default=False)
    confirmed_date = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    # REQUIRED_FIELDS = ['full_name'] #['full_name'] #python manage.py createsuperuser

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

    @property
    def active(self):
        return self.active
