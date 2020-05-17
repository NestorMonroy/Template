from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView

from .mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm, RegisterForm
from .signals import user_logged_in


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form,):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            # print("nestor Login usuario 1")
            # print(user)
            # pendiente ya que esta regresando una nueva session key para cada usuario
            # print(request.session.session_key)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


def logout_view(request):
    logout(request)
    return redirect("/")
