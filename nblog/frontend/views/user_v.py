from django.conf import settings
from django.core.mail import send_mail

from django.shortcuts import redirect, render

def home_page(request):
    # print(request.session.get("first_name", "Unknown"))
    # request.session['first_name']
    context = {
        "title":"Hello World!",
        "content":" Welcome to the homepage.",

    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAHHHHHH"
    return render(request, "index.html", context)


def emailsending(request):
    subject = "Thank you otro"
    message = "You have otro"
    email_from = settings.EMAIL_HOST_USER
    toaddress = ['nestor.monroy.90@gmail.com']
    send_mail(subject, message, email_from, toaddress)
    return render(request, 'frontend/otro.html')
