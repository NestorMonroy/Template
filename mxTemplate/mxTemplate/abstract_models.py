from django.db import models
from django.utils import timezone
from django.conf import settings


User = settings.AUTH_USER_MODEL


class DefaultBasicModelSec(models.Model):
    active = models.BooleanField(default=True, verbose_name='estado del sitio')
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    user_account = models.IntegerField(blank=True,null=True)
    user_modify = models.IntegerField(blank=True,null=True)
    
    class Meta:
        abstract = True