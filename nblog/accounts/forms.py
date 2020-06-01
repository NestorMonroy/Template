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


class ProfileForm(BaseForm, forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=models.User.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = models.Profile
        fields = ['user', 'bio', 'city', 'avatar', ]


class SignUpForm(BaseForm, UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, label='Nombre (s)')
    last_name = forms.CharField(
        max_length=30, required=False, label='Apellido')
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    username = forms.EmailField(required=True, label='Email')

    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data['username']
        if '@' in email:
            return email

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        if password != confirm_password:
            self.add_error('password2', 'Οι κωδικοί δε ταιριάζουν')
        return cleaned_data


class SignUpFormEng(SignUpForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'


class ProfileForm(BaseForm, forms.ModelForm):
    user = forms.ModelChoiceField(queryset=models.User.objects.filter(
        is_staff=False), widget=forms.HiddenInput(), required=False)

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


class RegisterForm(forms.Form):
    # username = forms.CharField(label='Username', max_length=100)
    firstname = forms.CharField(label="First Name", max_length=100)
    lastname = forms.CharField(label="Last Name", max_length=100)
    email = forms.EmailField(label='Email')
    username = forms.CharField(label='Username', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class Step1Form(forms.Form):
    avatar = forms.ImageField(label='Avatar')


class Step2Form(forms.Form):
    token = forms.CharField(max_length=100)
