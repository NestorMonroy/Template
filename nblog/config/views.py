from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect

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
