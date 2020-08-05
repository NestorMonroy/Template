import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.decorators import action

from rest_framework import views, viewsets, mixins, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from nblog.accounts.views.permissions import IsAuthorOrReadOnly
from accounts.views.permission import IsAuthorOrReadOnly
from rest_framework.response import Response
from ..forms import PostForm
from ..models import Post, Rating
from ..serializers import (
    PostSerializer,
    RatingSerializer,
    PostActionSerializer,
    PostCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


User = get_user_model()

# class BasePostAttrViewSet(viewsets.GenericViewSet,
#                             mixins.ListModelMixin,
#                             mixins.CreateModelMixin):
#     """Base viewset for user owned recipe attributes"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthorOrReadOnly,)

#     def get_queryset(self):
#         """Return objects for the current authenticated user only"""
#         return self.queryset.filter(user=self.request.user).order_by('-name')

#     def perform_create(self, serializer):
#         """Create a new object"""
#         serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Manage the post in the database"""
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(methods=['POST'], detail=True)
    def rate_post(self, request, pk=None):
        if 'stars' in request.data:
            response ={'message':'work'}
            post = Post.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            # print(user.id)
            try:
                rating = Rating.objects.get(user=user.id, post=post.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many= False)
                response={'message':'Rating updated', 'result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, post=post, stars=stars)
                serializer = RatingSerializer(rating, many= False)
                response={'message':'Rating created', 'result':serializer.data}
                return Response(response, status=status.HTTP_200_OK)
                

        else:
            response ={'message':'Necesitas agregar stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



    def get_queryset(self):
        user = self.request.user.id
        # print(user, 'nl')
        if user != None:
            return self.queryset.by_id(user)
        else:
            return self.queryset

    def perform_create(self, serializer):
        """Create a new post"""
        serializer.save(user=self.request.user)
    

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        """Create a new rating"""
        serializer.save(user=self.request.user)

    def update(self, request, *arg, **kwargs):
            response ={'message':'You cant update ratings like that'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *arg, **kwargs):
            response ={'message':'You cant vreate ratings like that'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)