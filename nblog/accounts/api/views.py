
from django.shortcuts import resolve_url
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, QueryDict
from django.conf import settings

from django.views.generic.edit import FormView
from django.views.generic import View, ListView, DetailView

from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)

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
from ..forms import LoginForm, SignUpForm, ProfileFrontEndForm, UpdatePasswordForm, ForgotPasswordForm

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
    form_title, form_button = 'Δημιουργια Λογαριασμου', 'Δημιουργια'
    text = '''Δημιουργώντας λογαριασμό στο κατάστημα μας, θα μπορείτε να ολοκληρλωσετε πιο εύκολα την διαδικασία παραγγελίας,
              να προσθέσετε προϊόντα στο λιστα Επιθυμιών και πολλά άλλα.'''
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user_ = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            send_mail('Ευχαριστουμε που εγγραφήκατε στο optika-kotsalis.',
                      f'To username σας είναι {username}',
                      SITE_EMAIL,
                      [username, ],
                      fail_silently=True
                      )
            return redirect('user_profile')
    else:
        messages.warning(request, form.errors)
    context = locals()
    return render(request, 'frontend/user_views/register.html', context)

