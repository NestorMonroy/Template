from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)


User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email...'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password...'
        })
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/
            not_active = qs.filter(is_active=False)
            user = authenticate(request, username=email, password=password)
            # print(user)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        self.user = user
        return data


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

    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre'
    }))

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password1', 'password2')

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
