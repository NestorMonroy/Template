from django.conf.urls import include, url
from django.urls import path, re_path

from frontend.views import (user_v)


urlpatterns = [
    # url(r'^logout/$', user_views.logout, name='logout'),
    # path('login/', user_views.login, name='login'),
    # # url(r'^login/2fa$', user_views.Login2FAView.as_view(), name='auth.login.2fa'),
    # url(r'^register/$', user_views.register, name='register'),
    # url(r'^signup/$', user_views.signup_view, name='signup'),
    url(r'^otro/$', user_v.emailsending, name='otro'),

]
