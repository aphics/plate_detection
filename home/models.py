from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CarHistory(models.Model):
    class VehicleOptions(models.TextChoices):
        CAR = "car", _("Car")
        MOTORCYCLE = "mot", _("Motorcycle")
        AUTOBUS = "bus", _("Autobus")
        TRUCK = "tru", _("Truck")
        OTHER = "oth", _("Other")

    vehicle_plate = models.CharField(max_length=20)
    vehicle_color = models.CharField(max_length=20)
    vehicle_type = models.CharField(
        max_length=3, choices=VehicleOptions.choices, default=VehicleOptions.CAR
    )
    created_date = models.DateTimeField(timezone.now())
    entry_date = models.DateTimeField(null=True, blank=True)
    exit_date = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    

    def __str__(self):
        return self.vehicle_plate

    class Meta:
        verbose_name_plural = "Historial de accesos"
