import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..forms import PostForm
from ..models import Post
from ..serializers import (
    PostSerializer, 
    PostActionSerializer,
    PostCreateSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['POST']) # http method the client == POST
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated]) # REST API course
def post_create_view(request, *args, **kwargs):
    serializer = PostCreateSerializer(data=request.POST)
    print(serializer)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def posts_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    username = request.GET.get('username') # ?username=Justin
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)


@api_view(['GET'])
def post_detail_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete_view(request, tweet_id, *args, **kwargs):
    qs = Post.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet removed"}, status=200)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def post_action_view(request, *args, **kwargs):
#     '''
#     id is required.
#     Action options are: like, unlike, retpost
#     '''
#     serializer = PostActionSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         data = serializer.validated_data
#         tweet_id = data.get("id")
#         action = data.get("action")
#         content = data.get("content")
#         qs = Post.objects.filter(id=tweet_id)
#         if not qs.exists():
#             return Response({}, status=404)
#         obj = qs.first()
#         if action == "like":
#             obj.likes.add(request.user)
#             serializer = PostSerializer(obj)
#             return Response(serializer.data, status=200)
#         elif action == "unlike":
#             obj.likes.remove(request.user)
#             serializer = PostSerializer(obj)
#             return Response(serializer.data, status=200)
#         elif action == "repost":
#             new_post = Post.objects.create(
#                     user=request.user, 
#                     parent=obj,
#                     content=content,
#                     )
#             serializer = PostSerializer(new_post)
#             return Response(serializer.data, status=201)
#     return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = PostSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)


# def posts_list_view(request, *args, **kwargs):
#     qs = Post.objects.all()
#     post_list = [x.serialize() for x in qs ]

#     data = {
#         "isUser":False,
#         "response": post_list
#     }
#     return JsonResponse(data)
#     # return render(request, "post/list.html")


# def post_create_view(request, *arg, **kwargs):
#     user = request.user
#     if not request.user.is_authenticated:
#         user = None
#         if request.is_ajax():
#             return JsonResponse({}, status=401)
#         return redirect(settings.LOGIN_URL)
#     print("ajax", request.is_ajax(), request.user)
#     form = PostForm(request.POST or None)
#     next_url = request.POST.get("next") or None
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.user = user or None
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201) # 201 == created items
#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#             return redirect(next_url)
#         form = PostForm()
#     if form.errors:
#         if request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#     return render(request, 'post/components/forms.html', context={"form":form})


def posts_detail_view(request, post_id, *args, **kwargs):
    data = {
        "id":post_id,
    }
    status = 200    
    try:
        obj = Post.objects.get(id=post_id)
        data['content'] = obj.content
        # data['user'] = obj.user
    except:
        data['message'] = "Not found"
        status = 400

        # raise Http404
    return JsonResponse(data, status=status)
    

#     # return HttpResponse(f"<h1>Hello -{post_id} --{obj.content} --{obj.user} </h1>")


#     # return render(request, "post/detail.html", context={"post_id": post_id})
