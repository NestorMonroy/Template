
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render, HttpResponseRedirect, get_object_or_404
import uuid

from django.http import HttpResponseRedirect, QueryDict
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail


from django.views.generic.edit import FormView
from django.views.generic import View, ListView, DetailView

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

from .. import models
from ..forms import LoginForm, SignUpForm, ProfileFrontEndForm, UpdatePasswordForm, ForgotPasswordForm, RegisterForm, Step1Form, Step2Form
from ..emails import send_password_reset_email, send_account_activate_email
from .decorators import anonymous_required

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


@method_decorator(login_required, name='dispatch')
class UserDashboardView(ListView):
    template_name = 'accounts/dashboard.html'
    model = models.Profile

    def get_queryset(self):
        profile = self.request.user.profile
        return models.Profile.objects.filter()[:5]

    def get_context_data(self, **kwargs):
        context = super(UserDashboardView, self).get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile
        context.update(locals())
        return context


def register_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect('/')
    form_title, form_button = 'Crear una cuenta', 'Creación'
    text = '''Creando una cuenta en nuestro blog'''
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user_ = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            send_mail('Gracias por registrate',
                      f'Tu username es {username}',
                      SITE_EMAIL,
                      [username, ],
                      fail_silently=True
                      )
            return redirect('accounts:user_profile')
    else:
        messages.warning(request, form.errors)
    context = locals()
    return render(request, 'accounts/register.html', context)


def registerHandler(request):
    if settings.SIGN_UP_LOCKED:
        return render(request, 'registration/disabled.html')
    form = None
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Check for dupe users
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            users = models.User.objects.filter(email=email)
            if len(users) > 0:
                # User already exists with this email
                form.add_error(
                    None, 'User exists with that email already. Did you mean to login?')
                return render(request, 'registration/register.html', {'form': form})
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['email'][:30]
            password = form.cleaned_data['password']

            # Shiny new saved user
            user = models.Profile.new(
                username, email, password, firstname, lastname)

            # Email activation
            token = models.AccountActivationToken(
                user=user, token=uuid.uuid4())
            token.save()
            send_account_activate_email(request, token)

            user = authenticate(username=username, password=password)
            login(request, user)
            continue_url = request.GET.get('next')
            if continue_url:
                return HttpResponseRedirect(continue_url)
            return HttpResponseRedirect('/register/step-1')
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        else:
            form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def handle_uploaded_file(f, filename):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def handle_uploaded_file(f, filename):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def step1Handler(request):
    if request.method == 'POST':
        form = Step1Form(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile.avatar = form.cleaned_data['avatar']
            request.user.profile.save()
        return redirect(reverse('accounts:register-step-2'))
    else:
        form = Step1Form()
    return render(request, 'registration/step-1.html')


@login_required
def step2Handler(request):
    if request.method == 'POST':
        form = Step2Form(request.POST)
        # if form.is_valid():
        # 	source = customer.sources.create(source=form.cleaned_data['token'])
        # 	if request.user.customer.default_source == '':
        # 		request.user.customer.default_source = source.get('id')
        # 		request.user.customer.save()
        return redirect(reverse('core:home'))
    else:
        form = Step1Form()
    return render(request, 'registration/step-2.html')


def logoutHandler(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def profileHandler(request):
    form = ProfileForm()
    return render(request, 'user/user_settings_profile.html', {'form': form})


@login_required
def userHandler(request, user_id):
    user = get_object_or_404(models.User, pk=user_id)
    return render(request, 'user/user.html', {'user': user})


def resetPasswordFormHandler(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = models.User.objects.filter(email=email)
            if len(users) < 1:
                # No user, fail
                form.add_error(None, 'No user exists with that email.')
                return render(request, 'registration/reset_password.html', {'form': form})
            user = users[0]
            passResetToken = models.PasswordResetToken.objects.filter(
                user=user)
            if len(passResetToken) < 1:
                passResetToken = models.PasswordResetToken.new(user)
                send_password_reset_email(request, passResetToken)
                passResetToken.save()
                return redirect(reverse('accounts:user_login'))
            else:
                form.add_error(
                    None, 'An email has already been sent to that email.')
    else:
        form = EmailForm()
    return render(request, 'registration/reset_password.html', {'form': form})


@anonymous_required()
def resetPasswordHandler(request, token):
    if request.method == 'GET':
        passResetToken = get_object_or_404(
            models.PasswordResetToken, token=token)
        if passResetToken:
            passResetToken.user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, passResetToken.user)
            passResetToken.delete()
            return redirect(reverse('posts:homepage') + '#/profile')
    return redirect(reverse('user:login'))


@login_required
def activeAccountHandler(request, token):
    if request.method == 'GET':
        activateAccountToken = get_object_or_404(
            models.AccountActivationToken, token=token)
        if activateAccountToken:
            activateAccountToken.user.profile.active = True
            activateAccountToken.user.profile.save()
            activateAccountToken.delete()
    return redirect(reverse('posts:homepage'))
