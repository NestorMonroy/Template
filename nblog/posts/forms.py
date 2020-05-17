from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    publish = forms.DateField()

    class Meta:
        model = Post
        fields = ["title", "content", "image", "draft", "publish"]
