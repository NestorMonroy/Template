from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from django.views import generic

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect


from posts.models import Post

from ..forms import PostSerachForm
from django.utils import timezone

def post_index(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()  # .order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")

    context = {
        "object_list": query,
        "title": "List",
        # "page_request_var": page_request_var,
        "today": today,
    }
    return render(request, "index.html", context)
