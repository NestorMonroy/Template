from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_list,
    post_detail,
    post_update,
    post_delete,
    PostNew,
    PostEdit
)

urlpatterns = [
    url(r'^$', post_list, name='list'),
    url(r'^create/$', PostNew.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostEdit.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),
]
