
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from django.shortcuts import redirect, render
from django.utils.html import mark_safe

User = get_user_model()


def message_view(request, message=None, title=None):
    """
    provides a generic way to render any old message in a template
    (used for when a user is disabled, or unapproved, or unverified, etc.)
    """
    context = {"message": mark_safe(message), "title": title or settings.PROJECT_NAME}
    return render(request, "core/message.html", context)


def home_page(request):
    # print(request.session.get("first_name", "Unknown"))
    # request.session['first_name']
    context = {
        "title": "Hello World!",
        "content": " Welcome to the homepage.",

    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAHHHHHH"
    return render(request, "core/index.html", context)


class IndexView(TemplateView):

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.filter(is_active=True)
        # context["customers"] = Customer.objects.filter(is_active=True)
        return context
