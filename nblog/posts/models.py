from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django.db import models
from django.db.models.signals import pre_save

from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify


from markdown_deux import markdown
from comments.models import Comment

from .utils import get_read_time

from django.contrib.auth.models import User


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    PostModel = instance.__class__
    new_id = PostModel.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" % (new_id, filename)


class Category(models.Model):
    name = models.CharField('Nombre de la categoría', max_length=255)

    def __str__(self):
        """str."""
        return self.name


class Tag(models.Model):
    name = models.CharField('Nombre de etiqueta', max_length=255)

    def __str__(self):
        """str."""
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, verbose_name='Categoria', on_delete=models.PROTECT, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='Tags')
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    is_publick = models.BooleanField('¿Está abierto al público?', default=True)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    description = models.TextField('Descripción del articulo', blank=True)
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_at = models.DateTimeField(
        'Fecha de creación', default=timezone.now)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_description(self):
        if self.description:
            return self.description
        else:
            description = 'Categoria:{0} Etiquetas:{1}'
            category = self.category
            tags = ' '.join(tag.name for tag in self.tag.all())
            description = description.format(category, tags)
            return description

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    def get_api_url(self):
        return reverse("posts-api:detail", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    def get_next(self):
        next_post = Post.objects.filter(
            is_publick=True, created_at__gt=self.created_at
        ).order_by('-created_at')
        if next_post:
            return next_post.last()
        return None

    def get_prev(self):
        prev_post = Post.objects.filter(
            is_publick=True, created_at__lt=self.created_at
        ).order_by('-created_at')
        if prev_post:
            return prev_post.first()
        return None

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
