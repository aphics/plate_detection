from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import redirect, render


def home(request):
    return render(request, "home.html")
