
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone


class PostQuerySet(QuerySet):

    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostQuerySet, self).filter(draft=False).filter(publish__lte=timezone.now())

    def get_for_user(self, user):
        if user.id == None:
            return self.filter(is_public=True).active()


class ChannelQuerySet(QuerySet):
    def get_for_user(self, user):
        if user.id == None:
            return self.filter(public=True)
        else:
            return self.filter(Q(public=True) | Q(followers=user) | Q(enrollment=self.model.ENROLLMENTS.SELF)).distinct()


class TagQuerySet(QuerySet):
    def get_for_user(self, user):

        from .models import Post
        q_object = Q(post__channel__public=True) & Q(
            post__status=Post.STATUSES.PUBLISHED)

        if user.id is not None:
            q_object = Q(post__channel__followers=user.id) | q_object

        return self.filter(q_object).distinct().filter(post__published__lte=timezone.now())
