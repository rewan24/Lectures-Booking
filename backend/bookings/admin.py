from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("student", "group", "created_at")
    list_filter = ("group", "created_at")
    search_fields = ("student__full_name", "group__name")
