from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
)
from django.db.models import Q
from django.contrib.auth import get_user_model


from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework import status, viewsets

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)

from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination


User = get_user_model()


class UserLoginAPIView(APIView):

    serializer_classe = UserLoginSerializer

    def get(self, request, format=None):

        an_apiview = [
            'User HTTP methods as function (get, post, patch, put, delete'
        ]

        return Response({'mesagge': 'hello', 'an_apiview': an_apiview})

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():

            username = serializer.validated_data.get('username')
            message = f'Hello{username}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):

    def list(self, request):

        a_viewset = [
            'User list, create, retrive, update, partial'
        ]

        return Response({'message': 'HELLO', 'a_viewset': a_viewset})


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


# class UserLoginAPIView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = UserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             new_data = serializer.data
#             return Response(new_data, status=HTTP_200_OK)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# from django.contrib.auth import (
#     authenticate,
#     get_user_model,
#     login,
#     logout,

# )
# from django.shortcuts import render, redirect
# from django.utils.http import is_safe_url
# from django.views.generic import CreateView, FormView

# from .mixins import NextUrlMixin, RequestFormAttachMixin
# from .forms import LoginForm, RegisterForm
# from .signals import user_logged_in


# def login_view(request):
#     next = request.GET.get('next')
#     title = "Login"
#     form = LoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect("/")
#     return render(request, "accounts/login.html", {"form": form, "title": title})


# class RegisterView(CreateView):
#     form_class = RegisterForm
#     template_name = 'accounts/register.html'
#     success_url = '/login/'


# def logout_view(request):
#     logout(request)
#     return redirect("/")
