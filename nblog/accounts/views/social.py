from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import LogoutView

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.shortcuts import render
from ..models import ExamplePost
from ..forms import PostForm
from ..serializers import PostSerializer, UserSerializer, AuthTokenSerializer, RegistrationSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = UserSerializer


class RegistrationAPIView(APIView):
    
    def post(self, request):
        print(self, "nestor")
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("#Incoming Request#\nType: Register\nUser: "+str(user.id)+"\n#End Request")
            return Response({'token': Token.objects.get(user=user).key,"userEmail":user.email,"userId":user.id},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def home_users(request):
    tmpl_vars = {'form': PostForm()}
    return render(request, 'accounts/index.html', tmpl_vars)

############################
### function based views ###
############################


@api_view(['GET', 'POST'])
def post_collection(request):
    if request.method == 'GET':
        posts = ExamplePost.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'text': request.DATA.get('the_post'), 'author': request.user}
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def post_element(request, pk):

    post = get_object_or_404(Post, id=pk)

    # try:
    #     post = Post.objects.get(pk=pk)
    # except Post.DoesNotExist:
    #     return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #########################
### class based views ###
#########################

# class PostCollection(generics.ListCreateAPIView):
#     queryset = ExamplePost.objects.all()
#     serializer_class = PostSerializer


# class PostMember(generics.RetrieveDestroyAPIView):
#     queryset = ExamplePost.objects.all()
#     serializer_class = PostSerializer

# class PostCollection(mixins.ListModelMixin,
#                      mixins.CreateModelMixin,
#                      generics.ListAPIView):

#     queryset = ExamplePost.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class PostMember(mixins.RetrieveModelMixin,
#                  mixins.DestroyModelMixin,
#                  generics.GenericAPIView):

#     queryset = ExamplePost.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
