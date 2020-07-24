from django.contrib import admin
from .models import ExamplePost, User
# from dj_rest_auth.models import TokenModel
# Register your models here.
admin.site.register(ExamplePost)
admin.site.register(User)
# admin.site.register(TokenModel)