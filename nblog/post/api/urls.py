from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
