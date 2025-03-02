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

    def calculate_usage_time(self):
        if self.entry_date and self.exit_date:
            self.duracion = self.exit_date - self.entry_date
            self.save()

    @property
    def calculate_price(self, fee):
        if self.duracion:
            usage_time_hours = self.duracion.total_seconds() / 3600
            return round(usage_time_hours * fee, 2)
        return 0

    def __str__(self):
        return self.vehicle_plate

    class Meta:
        verbose_name_plural = "Historial de accesos"
