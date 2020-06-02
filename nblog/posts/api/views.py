from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, Http404

from ..models import Channel, Post, Tag


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        ret = super(IndexView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user).active()


class ChannelIndexView(ListView):
    model = Channel
    template_name = 'posts/channel_index.html'
    context_object_name = 'channel_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        qs = super(ChannelIndexView, self).get_queryset(*args, **kwargs)
        return qs.get_for_user(self.request.user)


class ChannelDetailView(ListView):
    model = Post
    template_name = 'posts/channel_view.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        self.channel = get_object_or_404(Channel.objects.get_for_user(
            user=self.request.user), slug=self.kwargs['slug'])
        response = super(ChannelDetailView, self).dispatch(
            request, *args, **kwargs)
        return response

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        ret = super(ChannelDetailView, self).get_queryset(*args, **kwargs)

        if ((self.channel.public) or (user in self.channel.followers.all())):
            return ret.filter(channel=self.channel).active()
        else:
            return ret.none()

    def get_context_data(self, **kwargs):
        context = super(ChannelDetailView, self).get_context_data(**kwargs)
        context['channel'] = self.channel
        return context


class PostIndexView(ListView):
    model = Post
    template_name = 'posts/post_index.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def get_queryset(self, *args, **kwargs):
        ret = super(PostIndexView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user).active()


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_view.html'
    context_object_name = 'post'

    def get_queryset(self, *args, **kwargs):
        ret = super(PostDetailView, self).get_queryset(*args, **kwargs)
        return ret.get_for_user(user=self.request.user).active()


def self_enrollment(request, *args, **kwargs):
    user = request.user
    if request.method == 'POST':
        channel = get_object_or_404(
            Channel.objects.get_for_user(user), slug=kwargs['slug'])
        channel.followers.add(user)
        return HttpResponseRedirect(reverse('mesh_channel_index'))
    else:
        return HttpResponseRedirect(reverse('mesh_channel_index'))


class TagDetailView(ListView):
    model = Post
    template_name = 'posts/tag_view.html'
    context_object_name = 'post_list'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):

        self.tag = get_object_or_404(Tag.objects.all(), slug=kwargs['slug'])
        response = super(TagDetailView, self).dispatch(
            request, *args, **kwargs)
        return response

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        ret = super(TagDetailView, self).get_queryset(
            *args, **kwargs).get_for_user(user).filter(tags=self.tag).distinct()

        if len(ret) == 0:
            raise Http404
        return ret

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class TagIndexView(ListView):
    model = Tag
    template_name = 'posts/tag_index.html'
    context_object_name = 'tag_list'

    def get_queryset(self, *args, **kwargs):
        qs = super(TagIndexView, self).get_queryset(*args, **kwargs)
        return qs.get_for_user(self.request.user)
