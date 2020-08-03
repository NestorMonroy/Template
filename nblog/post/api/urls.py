from django.conf.urls import include, url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='post')
router.register('ratings', views.RatingViewSet, basename='ratings')

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]
