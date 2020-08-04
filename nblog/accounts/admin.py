from django.contrib import admin
from .models import  User
# from dj_rest_auth.models import TokenModel
# Register your models here.
admin.site.register(User)
# admin.site.register(TokenModel)