from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import math


class CarHistory(models.Model):
    current_fee = 12

    ICONOS_VEHICULO = {
        "car": "fa-car-side",
        "mot": "fa-motorcycle",
        "bus": "fa-bus",
        "tru": "fa-truck",
        "oth": "fa-question",
    }

    class VehicleOptions(models.TextChoices):
        CAR = "car", _("Auto")
        MOTORCYCLE = "mot", _("Moto")
        AUTOBUS = "bus", _("Autobus")
        TRUCK = "tru", _("Truck")
        OTHER = "oth", _("Otro")

    vehicle_plate = models.CharField(max_length=20)
    vehicle_color = models.CharField(max_length=20)
    vehicle_rgb = models.CharField(max_length=20)
    vehicle_type = models.CharField(
        max_length=3, choices=VehicleOptions.choices, default=VehicleOptions.CAR
    )
    created_date = models.DateTimeField(null=True, blank=True)
    entry_date = models.DateTimeField(null=True, blank=True)
    image_entry_vehicle = models.ImageField(
        upload_to="images_entry_vehicles/", null=True, blank=True
    )
    image_entry_plate = models.ImageField(
        upload_to="images_entry_plates/", null=True, blank=True
    )
    exit_date = models.DateTimeField(null=True, blank=True)
    image_exit_vehicle = models.ImageField(
        upload_to="images_exit_vehicles", null=True, blank=True
    )
    image_exit_plate = models.ImageField(
        upload_to="images_exit_plates/", null=True, blank=True
    )
    usage_time = models.DurationField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    fee = models.FloatField(null=True, blank=True)

    def get_usage_time(self):
        if self.exit_date:
            return self.exit_date - self.entry_date
        else:
            return timezone.now() - self.entry_date

    def get_price(self):
        usage_time = self.get_usage_time()
        if usage_time:
            total_hours = usage_time.total_seconds() / 3600
            horas_cobradas = math.ceil(total_hours)  # Redondear hacia arriba
            return horas_cobradas * self.fee
        return 0

    def get_vehicle_icon(self):
        return self.ICONOS_VEHICULO.get(self.vehicle_type, "fa-question")

    def __str__(self):
        return self.vehicle_plate

    class Meta:
        verbose_name_plural = "Historial de accesos"
