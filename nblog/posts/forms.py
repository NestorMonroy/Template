import datetime
from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Titulo' }))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder':'Contenido'}))

    # image = forms.ImageField(widget=forms.ClearableFileInput(
    #     attrs={'multiple': True, 'placeholder':'Contenido2'}))

    publish = forms.DateField(widget=forms.SelectDateWidget(
        attrs={ 'style': 'display: inline-block; width: 33%;','class': 'form-control'}))
    
    draft = forms.CharField(widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), label='draft')
    

    class Meta:
        model = Post
        fields = ["title", "content", "image", "draft", "publish"]

    """
        class ImageForm(forms.ModelForm):
        image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        )
    """
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in iter(self.fields):
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control'
    #         })

    # def __init__(self, *args, **kwargs):
    #     super(PostForm).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('title', css_class='form-group col-md-6 mb-0'),
    #             Column('content', css_class='form-group col-md-6 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('image', css_class='form-group col-md-6 mb-0'),
    #             Column('draft', css_class='form-group col-md-4 mb-0'),
    #             Column('title', css_class='form-group col-md-4 mb-0'),

    #             css_class='form-row'
    #         ),
    #         # CustomCheckbox('draft'),  # <-- Here
    #         Submit('submit', 'Sign in')
    #     )
