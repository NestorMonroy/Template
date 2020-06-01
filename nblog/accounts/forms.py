from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from . import models


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ForgotPasswordForm(BaseForm):
    email = forms.EmailField(required=True)


class LoginForm(BaseForm):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class SignUpForm(BaseForm, UserCreationForm):

    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    full_name = forms.CharField(
        max_length=150, required=False, label='Nombre')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ['email', 'full_name', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        if password != confirm_password:
            self.add_error('password2', 'Passwords dont match')
        return cleaned_data


class SignUpFormEng(SignUpForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'


class ProfileForm(BaseForm, forms.ModelForm):
    user = forms.ModelChoiceField(queryset=models.User.objects.filter(
        staff=False), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.Profile
        fields = ['user', 'bio', 'city', 'avatar', ]


class ProfileFrontEndForm(BaseForm, forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=models.User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = models.Profile
        fields = ['user', 'bio', 'city', 'avatar', ]


class ProfileFrontEndEngForm(ProfileFrontEndForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].label = 'First Name'
        self.fields['bio'].label = 'Last Name'
        self.fields['city'].label = 'Shipping Address'
        self.fields['avatar'].label = 'Shipping City'


class UpdatePasswordForm(BaseForm, PasswordChangeForm):
    pass




class Step1Form(forms.Form):
    avatar = forms.ImageField(label='Avatar')


class Step2Form(forms.Form):
    token = forms.CharField(max_length=100)
