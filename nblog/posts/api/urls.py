from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include


from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="homepage"),
    url(r'^channels/$', views.ChannelIndexView.as_view(), name="channel_index"),
    url(r'^channels/(?P<slug>.*)/$', views.ChannelDetailView.as_view(), name="channel_detail"),
    url(r'^follow/(?P<slug>.*)/$', views.self_enrollment, name="follow_channel"),
    url(r'^posts/$', views.PostIndexView.as_view(), name="post_index"),
    url(r'^posts/(?P<slug>.*)/$', views.PostDetailView.as_view(), name="post_detail"),
    url(r'^tags/(?P<slug>.*)/$' , views.TagDetailView.as_view(), name="tag_view"),
    url(r'^tags/$', views.TagIndexView.as_view(), name="mesh_tag_index"),
]
