from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import redirect, render


def home(request):
    return render(request, "dashboard.html")


def entry(request):
    return render(request, "entry.html")


def exit(request):
    return render(request, "exit.html")


def users(request):
    return render(request, "users.html")


def plates(request):
    return render(request, "plates.html")
