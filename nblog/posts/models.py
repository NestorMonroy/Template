import os
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.db.models.signals import pre_save
from model_utils import Choices

from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown
from comments.models import Comment

from .utils import get_read_time, upload_image_path, unique_slug_generator, upload_icon_path

from accounts.models import User

from .managers import PostQuerySet, ChannelQuerySet, TagQuerySet


class Enrollments(models.TextChoices):
    SELF = '0', "Self",
    AUTHOR = '1' "Author",


class _Abstract(models.Model):  # microblog compatible.
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=140, unique=True)
    text = models.TextField(default='')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Channel(_Abstract):
    ENROLLMENTS = Choices(
        (0, 'SELF', 'Self'),
        (1, 'AUTHOR', 'Author'),
    )
    followers = models.ManyToManyField(User)
    public = models.BooleanField(
        default=True, help_text="If False, only followers will be able to see content.")

    enrollment = models.IntegerField(
        default=ENROLLMENTS.SELF, choices=ENROLLMENTS)

    objects = ChannelQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('channel_view', kwargs={'slug': self.slug, })

    class Meta:
        ordering = ['title']


class Tag(_Abstract):

    objects = TagQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('tag_view', kwargs={'slug': self.slug, })


class Post(_Abstract):

    SUMMARY_LENGTH = 50

    STATUSES = Choices(
        (0, 'DRAFT',     'Draft',),
        (1, 'PUBLISHED', 'Published',),
    )

    # channel = models.ForeignKey(
    #     Channel, on_delete=models.CASCADE,),
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,)
    status = models.IntegerField(
        default=STATUSES.DRAFT, choices=STATUSES,)
    custom_summary = models.TextField(default='')
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    tags = models.ManyToManyField(Tag)

    objects = PostQuerySet.as_manager()

    def _get_teaser(self):
        "A small excerpt of text that can be used in the absence of a custom summary."
        return self.text[:Post.SUMMARY_LENGTH]

    teaser = property(_get_teaser)

    def _get_summary(self):
        "Returns custom_summary, or teaser if not available."
        if len(self.custom_summary) > 0:
            return self.custom_summary
        else:
            return self.teaser

    summary = property(_get_summary)

    def get_absolute_url(self):
        return reverse('post_view', kwargs={'slug': self.slug, })


class File(models.Model):
    """Adjuntos asociados con artículos y comentarios"""
    title = models.CharField('título', max_length=255, blank=True)
    src = models.FileField('Adjunto archivo', upload_to='files/%Y/%m/%d/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(
        'Fecha de creación', default=timezone.now)

    def __str__(self):
        return 'modelo:{} pk:{} url:{}'.format(self.content_type, self.object_id, self.src.url)

    def get_filename(self):
        """Obtener el nombre del archivo"""
        return os.path.basename(self.src.url)


class Comment(models.Model):
    """Comentario"""
    name = models.CharField('nombre', max_length=255, default='Sin nombre')
    text = models.TextField('comentario')
    icon = models.ImageField(
        'miniatura', upload_to='comment_thumbnail/%Y/%m/%d/', blank=True, null=True)
    target = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='Artículo objetivo')
    files = GenericRelation('File')
    created_at = models.DateTimeField(
        'Fecha de creación', default=timezone.now)

    def __str__(self):
        return self.text[:10]

    def get_filename(self):
        """Obtener el nombre del archivo"""
        return os.path.basename(self.file.url)
