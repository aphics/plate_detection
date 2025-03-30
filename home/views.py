import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .models import CarHistory
from .plate_recognition import LicencePlateRecognition


@login_required
def home(request):
    return render(request, "dashboard.html")


@login_required
def entry(request):
    if request.method == "POST" and request.FILES.get("entry_image"):
        image_file = request.FILES["entry_image"]
        print(image_file)

        # Guardar imagen en temporal
        filename = f"entry_image.jpg"
        save_path = os.path.join("media/uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Procesar imagen
        lpr = LicencePlateRecognition()
        text_plate, detected_color, cls_vehicle = lpr.process_image(
            image_path=save_path, type_process="entry"
        )
        if text_plate == "No detectada":
            return render(
                request,
                "entry.html",
                {
                    "image_url": save_path,
                    "alerta": "no_vehiculo",
                    "vehicle": None,
                },
            )
        image_url = "media/uploads/processed_entry_image.jpg"
        existing_vehicle = CarHistory.objects.filter(
            vehicle_plate=text_plate,
            vehicle_color=detected_color,
            vehicle_type=cls_vehicle,
            exit_date__isnull=True,
        )
        if existing_vehicle.exists():
            return render(
                request,
                "entry.html",
                {
                    "image_url": image_url,
                    "alerta": "duplicado",
                    "vehicle": existing_vehicle[0],
                },
            )
        vehicle = CarHistory.objects.create(
            vehicle_plate=text_plate,
            vehicle_color=detected_color,
            vehicle_type=cls_vehicle,
            created_date=timezone.now(),
            entry_date=timezone.now(),
        )
        return render(
            request,
            "entry.html",
            {"image_url": image_url, "alerta": "exito", "vehicle": vehicle},
        )
    return render(request, "entry.html")


@login_required
def exit(request):
    if request.method == "POST" and request.FILES.get("exit_image"):
        image_file = request.FILES["exit_image"]
        print(image_file)

        # Guardar imagen en temporal
        filename = f"exit_image.jpg"
        save_path = os.path.join("media/uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Procesar imagen
        lpr = LicencePlateRecognition()
        text_plate, detected_color, cls_vehicle = lpr.process_image(
            image_path=save_path, type_process="exit"
        )
        if text_plate == "No detectada":
            return render(
                request,
                "exit.html",
                {
                    "image_url": save_path,
                    "alerta": "no_vehiculo",
                    "vehicle": None,
                },
            )
        image_url = "media/uploads/processed_exit_image.jpg"
        existing_vehicle = CarHistory.objects.filter(
            vehicle_plate=text_plate,
            vehicle_color=detected_color,
            vehicle_type=cls_vehicle,
            exit_date__isnull=True,
        )
        if existing_vehicle.exists():
            vehicle = existing_vehicle[0]
            vehicle.exit_date = timezone.now()
            vehicle.calculate_usage_time()
            vehicle.calculate_price(fee=42)

            vehicle.save()
            return render(
                request,
                "exit.html",
                {
                    "image_url": image_url,
                    "alerta": "exito",
                    "vehicle": vehicle,
                },
            )
        if len(existing_vehicle) == 0:
            vehiculo_temporal = CarHistory(
                vehicle_plate=text_plate,
                vehicle_color=detected_color,
                vehicle_type=cls_vehicle,
            )
            return render(
                request,
                "exit.html",
                {
                    "image_url": image_url,
                    "alerta": "no_encontrado",
                    "vehicle": vehiculo_temporal,
                },
            )

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
