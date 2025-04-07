from django.contrib import admin

# Register your models here.
from .models import CarHistory


@admin.register(CarHistory)
class CarHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "vehicle_plate",
        "vehicle_color",
        "vehicle_rgb",
        "vehicle_type",
        "created_date",
        "entry_date",
        "exit_date",
        "usage_time",
        "price",
        "fee",
    )
    list_filter = ("vehicle_color", "vehicle_type")
    search_fields = ("vehicle_plate",)
    ordering = ("-entry_date",)
    date_hierarchy = "entry_date"
