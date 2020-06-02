from django.contrib import admin

# Register your models here.
from . import models


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]

    search_fields = ["title", "content"]

    class Meta:
        model = models.Post


admin.site.register(models.Post, PostModelAdmin)
admin.site.register(models.Channel)
admin.site.register(models.Tag)
