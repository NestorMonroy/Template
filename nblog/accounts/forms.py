from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from . import models

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(LoginForm, self).clean(*args, **kwargs)



class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'password'
    }))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Repite password'
    }))

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):

        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.is_active = False
        if commit:
            user.save()
        return user



class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=False), widget=forms.HiddenInput(), required=False)

    class Meta:
        model = models.Profile
        fields = ('user', 'bio', 'city', 'avatar')



