from django.contrib import admin
from .models import *
# Register your models here.


class PostLikeAdmin(admin.TabularInline):
    model = PostLike

class PostAdmin(admin.ModelAdmin):
    inlines = [PostLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__email']
    class Meta:
        model = Post

class RatingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    class Meta:
        model = Rating

admin.site.register(Post,PostAdmin)
admin.site.register(Rating,RatingAdmin)
