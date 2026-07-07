from django.contrib import admin
from .models import TrafficRecord


@admin.register(TrafficRecord)
class TrafficRecordAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "location", "vehicle_count", "vehicle_type", "weather", "road_condition")
    list_filter = ("location", "vehicle_type", "weather", "road_condition", "hour")
    search_fields = ("location", "vehicle_type", "weather")
