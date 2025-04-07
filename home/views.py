import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import datetime, timedelta
from collections import Counter

from .models import CarHistory
from .plate_recognition import LicencePlateRecognition


@login_required
def home(request):
    today = timezone.now().date()
    fecha_inicio_str = request.GET.get("fecha_inicio", today.replace(day=1).isoformat())
    fecha_fin_str = request.GET.get("fecha_fin", today.isoformat())

    fecha_inicio_dt = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
    fecha_fin_dt = datetime.strptime(fecha_fin_str, "%Y-%m-%d")

    monto_mensual = CarHistory.objects.filter(
        created_date__year=today.year,
        created_date__month=today.month,
    ).aggregate(Sum("price"))["price__sum"]

    monto_anual = CarHistory.objects.filter(
        created_date__year=today.year,
    ).aggregate(
        Sum("price")
    )["price__sum"]

    autos_estacionados = CarHistory.objects.filter(
        exit_date__isnull=True,
    ).count()
    capacidad_total = 70
    capacidad_ocupada = f"{round(autos_estacionados / capacidad_total * 100, 2)}"

    # Filtrar rango de fechas
    registros = CarHistory.objects.filter(
        created_date__gte=fecha_inicio_dt,
        created_date__lte=fecha_fin_dt + timedelta(days=1) - timedelta(microseconds=1),
    )
    monto_filtro = registros.aggregate(Sum("price"))["price__sum"]

    # Obtener registros filtrados por fecha
    registros = CarHistory.objects.filter(
        created_date__gte=fecha_inicio_dt,
        created_date__lte=fecha_fin_dt + timedelta(days=1) - timedelta(microseconds=1),
    )
    # Contar registros por día
    conteo_por_dia = Counter(
        r.created_date.date().strftime("%Y-%m-%d") for r in registros
    )
    # Obtener listas ordenadas por fecha
    fechas_graph = sorted(conteo_por_dia.keys())
    totales_graph = [conteo_por_dia[fecha] for fecha in fechas_graph]

    return render(
        request,
        "dashboard.html",
        {
            "monto_mensual": f"$ {monto_mensual if monto_mensual is not None else 0:,.2f}",
            "monto_anual": f"$ {monto_anual:,.2f}",
            "autos_estacionados": autos_estacionados,
            "capacidad_ocupada": capacidad_ocupada,
            "monto_filtro": monto_filtro,
            "registros": registros,
            "fecha_inicio": fecha_inicio_str,
            "fecha_fin": fecha_fin_str,
            "fee": CarHistory.current_fee,
            "fechas_graph": fechas_graph,
            "totales_graph": totales_graph,
        },
    )


@login_required
def entry(request):
    if request.method == "POST" and request.FILES.get("entry_image"):
        image_file = request.FILES["entry_image"]

        # Guardar imagen en temporal
        filename = f"entry_image.jpg"
        save_path = os.path.join("media/uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Procesar imagen
        lpr = LicencePlateRecognition()
        text_plate, detected_color, detected_rgb, cls_vehicle = lpr.process_image(
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
            vehicle_rgb=detected_rgb,
            vehicle_type=cls_vehicle,
            created_date=timezone.now(),
            entry_date=timezone.now(),
            fee=CarHistory.current_fee,
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

        # Guardar imagen en temporal
        filename = f"exit_image.jpg"
        save_path = os.path.join("media/uploads", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Procesar imagen
        lpr = LicencePlateRecognition()
        text_plate, detected_color, detected_rgb, cls_vehicle = lpr.process_image(
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
            vehicle.usage_time = vehicle.get_usage_time()
            vehicle.price = vehicle.get_price()

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
