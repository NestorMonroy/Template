import random
from django.conf import settings

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = settings.AUTH_USER_MODEL

# Create your models here.

class PostQuerySet(models.QuerySet):
    def by_email(self, email):
        return self.filter(user__email__iexact=email)

    def by_id(self, id):
        return self.filter(user__id__iexact=id)

    def feed(self, user):
        profiles_exist = user.following.exists()
        followed_users_id = []
        if profiles_exist:
            followed_users_id = user.following.values_list("user__id", flat=True) # [x.user.id for x in profiles]
        return self.filter(
            Q(user__id__in=followed_users_id) |
            Q(user=user)
        ).distinct().order_by("-timestamp")


class PostManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PostQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)
    



class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)



class Post(models.Model):

    # parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='post_user', blank=True, through=PostLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    other = models.CharField(blank=True, null=True, max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PostManager()
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-id']
    
    @property
    def is_repost(self):
        return self.parent != None
    
    def no_of_ratings(self):
        ratings = Rating.objects.filter(post=self)
        return len(ratings)
    
    def avg_ratings(self):
        ratings = Rating.objects.filter(post=self)
        sum = 0
        for rating in ratings:
            sum += rating.stars

        if len(ratings) > 0:
            return sum /len(ratings)
        else:
            return 0


        return sum /len(ratings)


    # def save(self, *args, **kwargs):
    #     super(Post, self).save(*args, **kwargs)


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=(('user', 'post'),)
        index_together=(('user', 'post'))
