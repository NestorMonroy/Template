from django.conf.urls import include, url
from django.urls import path, re_path
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from django.contrib.auth.views import LogoutView

from .views import (social)

urlpatterns = [
    # url(r'^accounts/', social.home_users, name='hu'),

    url(r'^api/v1/posts/$', social.post_collection, name='ps'),
    url(r'^api/v1/posts/(?P<pk>[0-9]+)$', social.post_element,name='pe' ),

    # url(r'^accounts/', social.home_users, name='home_users'),

#     path('auth/facebook/', social.FacebookLogin.as_view(), name='fb_login'),
#     # path('accounts/', include('allauth.urls')),
    url(r'^accounts/', include('dj_rest_auth.urls')),

#     path('auth/', include('dj_rest_auth.urls')),
#     path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('registration/', RegisterView.as_view(), name='account_signup'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

#     re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
#             name='account_email_verification_sent'),

#     re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
#             name='account_confirm_email'),



]


