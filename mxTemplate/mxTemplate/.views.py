from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
  context = {
    "title" :"Team"
  }
  return render(request, "base.html", context )