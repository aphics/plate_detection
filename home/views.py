from django.contrib.auth.models import User

# Create your views here.
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, "dashboard.html")


@login_required
def entry(request):
    return render(request, "entry.html")


@login_required
def exit(request):
    return render(request, "exit.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("/login")
