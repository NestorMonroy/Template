
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import redirect, render

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
