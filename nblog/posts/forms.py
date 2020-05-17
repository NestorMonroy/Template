from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.Textarea()
    #forms.CharField(label=label,required=False, widget=forms.Textarea, initial = initial)
    publish = forms.DateField()

    class Meta:
        model = Post
        fields = ["title", "content", "image", "draft", "publish"]
