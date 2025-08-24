from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.booking_list, name="booking-list"),
    path("<int:pk>/", views.booking_detail, name="booking-detail"),
]