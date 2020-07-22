from django import forms
from .models import ExamplePost


class PostForm(forms.ModelForm):
    class Meta:
        model = ExamplePost
        # exclude = ['author', 'updated', 'created', ]
        fields = ['text']
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'Say something...'}
            ),
        }