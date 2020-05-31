from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment
from .fields import SimpleCaptchaField


class PostForm(forms.ModelForm):
    content = forms.Textarea()
    #forms.CharField(label=label,required=False, widget=forms.Textarea, initial = initial)
    publish = forms.DateField()

    class Meta:
        model = Post
        fields = ["title", "content", "image", "draft", "publish"]


class PostSerachForm(forms.Form):
    """Formulario de búsqueda de artículos"""

    keyword = forms.CharField(
        label='palabra clave', required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control mr-sm-2', 'placeholder': 'クイックサーチ'}),
    )



class CommentCreateForm(forms.ModelForm):
    """Formulario de envío de comentarios"""

    captha = SimpleCaptchaField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Comment
        fields = ('name', 'text', 'icon')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
            }),
            'text': forms.Textarea(attrs={
                'class': "form-control",
            }),
            'icon': forms.ClearableFileInput(attrs={
                'class': "form-control-file",
            }),
        }

