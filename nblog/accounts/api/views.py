
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render, HttpResponseRedirect, get_object_or_404
import uuid

from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail


from django.views.generic.edit import FormView
from django.views.generic import View, ListView, DetailView, UpdateView

from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib import messages

from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_protect

from django.views.decorators.cache import never_cache

from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .. import models
from ..forms import LoginForm, SignUpForm, ProfileFrontEndForm, UpdatePasswordForm, ForgotPasswordForm, Step1Form, Step2Form
from ..emails import send_password_reset_email, send_account_activate_email
from ..decorators import anonymous_required

SITE_EMAIL = settings.SITE_EMAIL


class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}


class LoginView(SuccessURLAllowedHostsMixin, FormView):

    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'accounts/login.html'
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context


class ProfileCreateView(generic.UpdateView):
    model = models.Profile
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        full_name = form.cleaned_data['full_name']
        email = form.cleaned_data['email'][:30]
        password = form.cleaned_data['password1']
        user = models.Profile.new(full_name, email, password)
        print(user)
        print("nestor")

        obj = form.save(commit=False)
        obj.email = self.request.email
        obj.save()
        return super(ProfileCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:user_detail', kwargs={
            'pk': self.request.user.pk
        })


def logoutHandler(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


def register_view(request):

    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect('/')
    form_title, form_button = 'Create new Account', 'Create'
    text = '''Creating new account to our store you can do the checkout process more easy,
                add items to wishlist and many more.'''
    form = None
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():

            # email = form.cleaned_data.get('email')
            # full_name = form.cleaned_data.get('full_name')
            # password = form.cleaned_data.get('password1')
            print("1")
            print(user)
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email'][:30]
            password = form.cleaned_data['password1']
            user = models.Profile.new(full_name, email, password)
            print(user)
            print("nestor")

            user = authenticate(user=user, password=password)

            if user:
                login(request, user)
                send_mail('Ευχαριστουμε που εγγραφήκατε στο optika-kotsalis.',
                          f'To username σας είναι {email}',
                          SITE_EMAIL,
                          [email, ],
                          fail_silently=True
                          )
            return redirect('posts:homepage')
    else:
        form = SignUpForm()
    context = locals()
    return render(request, 'registration/register.html', context)


class ProfileListView(generic.ListView):
    model = models.Profile
    template_name = 'accounts/dashboard.html'

    def get_queryset(self):
        id = self.request.user.id
        return models.Profile.objects.filter(id=id)


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = 'accounts/update_user.html'

    def get_object(self, queryset=None):
        try:
            obj = self.request.user.profile
            return obj
        except ObjectDoesNotExist:
            return None
