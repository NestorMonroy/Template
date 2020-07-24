from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include, url
from .views import posts_detail_view,posts_list_view, post_create_view


urlpatterns = [
    path('', posts_list_view, name='list'),
    path('create', post_create_view, name='create'),

    path('<int:post_id>/', posts_detail_view, name='detail'),

]
