import datetime
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    # content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

        

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
