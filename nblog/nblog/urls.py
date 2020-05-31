"""nblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(
        r'^', include('puppies.api.urls')
    ),

    url(r'^comments/', include(('comments.urls', 'comments'), namespace='comments')),

    # url(r'^', include(('posts.urls', 'posts'), namespace='posts')),

    path('', include(('accounts.api.urls',
                                 'users-api'), namespace='users-api')),
    # url(r'^api/comments/', include(('comments.api.urls',
    #                                 'comments-api'), namespace='comments-api')),
    # url(r'^api/posts/', include(('posts.api.urls', 'posts-api'), namespace='posts-api')),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
