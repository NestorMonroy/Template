from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)

from posts.models import Post

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly

from .serializers import (
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer
)


class PostCreateAPIView(APIView):

    def get(self, request, format=None):

        an_apiview = [
            'User HTTP methods as function (get, post, patch, put, delete'
        ]

        return Response({'message': 'hello'})


# class PostCreateAPIView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     #permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)



# class PostListAPIView(ListAPIView):
#     serializer_class = PostListSerializer
#     filter_backends= [SearchFilter, OrderingFilter]
#     permission_classes = [AllowAny]
#     search_fields = ['title', 'content', 'user__first_name']
#     pagination_class = PostPageNumberPagination #PageNumberPagination

#     def get_queryset(self, *args, **kwargs):
#         #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
#         queryset_list = Post.objects.all() #filter(user=self.request.user)
#         query = self.request.GET.get("q")
#         if query:
#             queryset_list = queryset_list.filter(
#                     Q(title__icontains=query)|
#                     Q(content__icontains=query)|
#                     Q(user__first_name__icontains=query) |
#                     Q(user__last_name__icontains=query)
#                     ).distinct()
#         return queryset_list


# class PostDetailAPIView(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'slug'
#     permission_classes = [AllowAny]
#     #lookup_url_kwarg = "abc"


# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsOwnerOrReadOnly]
#     #lookup_url_kwarg = "abc"
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)
#         #email send_email


# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsOwnerOrReadOnly]
#     #lookup_url_kwarg = "abc"


# def post_list(request):
#     today = timezone.now().date()
#     queryset_list = Post.objects.active()  # .order_by("-timestamp")
#     if request.user.is_staff or request.user.is_superuser:
#         queryset_list = Post.objects.all()

#     query = request.GET.get("q")
#     if query:
#         queryset_list = queryset_list.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query) |
#             Q(user__first_name__icontains=query) |
#             Q(user__last_name__icontains=query)
#         ).distinct()
#     paginator = Paginator(queryset_list, 3)  # Show 25 contacts per page
#     page_request_var = "page"
#     page = request.GET.get(page_request_var)
#     try:
#         queryset = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         queryset = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         queryset = paginator.page(paginator.num_pages)
#     context = {
#         "object_list": queryset,
#         "title": "List",
#         "page_request_var": page_request_var,
#         "today": today,
#     }
#     return render(request, "posts/post_list.html", context)


# class PostNew(generic.CreateView):
#     model = Post
#     template_name = "posts/post_form.html"
#     context_object_name = "obj"
#     form_class = PostForm
#     success_message = "Categoria Creada Satisfactoriamente"

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


# def post_detail(request, slug=None):
#     instance = get_object_or_404(Post, slug=slug)
#     if instance.publish > timezone.now().date() or instance.draft:
#         if not request.user.is_staff or not request.user.is_superuser:
#             raise Http404
#     share_string = quote_plus(instance.content)

#     initial_data = {
#         "content_type": instance.get_content_type,
#         "object_id": instance.id
#     }

#     form = CommentForm(request.POST or None, initial=initial_data)

#     if form.is_valid() and request.user.is_authenticated:
#         c_type = form.cleaned_data.get("content_type")
#         content_type = ContentType.objects.get(model=c_type)
#         obj_id = form.cleaned_data.get('object_id')
#         content_data = form.cleaned_data.get("content")
#         parent_obj = None
#         try:
#             parent_id = int(request.POST.get("parent_id"))
#         except:
#             parent_id = None

#         if parent_id:
#             parent_qs = Comment.objects.filter(id=parent_id)
#             if parent_qs.exists() and parent_qs.count() == 1:
#                 parent_obj = parent_qs.first()

#         new_comment, created = Comment.objects.get_or_create(
#             user=request.user,
#             content_type=content_type,
#             object_id=obj_id,
#             content=content_data,
#             parent=parent_obj,
#         )
#         return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

#     comments = instance.comments
#     context = {
#         "title": instance.title,
#         "instance": instance,
#         "share_string": share_string,
#         "comments": comments,
#         "comment_form": form,
#     }
#     return render(request, "posts/post_detail.html", context)


# class PostEdit(LoginRequiredMixin, generic.UpdateView):
#     model = Post
#     template_name = "posts/post_form.html"
#     context_object_name = 'obj'
#     form_class = PostForm
#     success_message = "Editado"
#     login_url = "login"

#     def form_valid(self, form):
#         form.instance.user_modify = self.request.user.id
#         # print(self.request.user.id)
#         return super().form_valid(form)


# def post_update(request, slug=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(Post, slug=slug)
#     form = PostForm(request.POST or None,
#                     request.FILES or None, instance=instance)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(request, "<a href='#'>Item</a> Saved",
#                          extra_tags='html_safe')
#         return HttpResponseRedirect(instance.get_absolute_url())

#     context = {
#         "title": instance.title,
#         "instance": instance,
#         "form": form,
#     }
#     return render(request, "posts/post_form.html", context)


# def post_delete(request, slug=None):
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
#     instance = get_object_or_404(Post, slug=slug)
#     instance.delete()
#     messages.success(request, "Successfully deleted")
#     return redirect("posts:list")
