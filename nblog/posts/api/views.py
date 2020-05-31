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

from posts.models import Post

from ..forms import PostSerachForm


class IndexView(generic.ListView):
    model = Post
    template_name = 'frontend/base.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        ret = super(IndexView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user)
