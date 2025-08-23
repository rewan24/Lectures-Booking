from rest_framework import generics, permissions
from .models import Booking
from .serializers import BookingSerializer


class BookingListCreateView(generics.ListCreateAPIView):
    """عرض وإنشاء الحجوزات"""
    queryset = Booking.objects.all().select_related("student", "group")
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]  # غيرها حسب احتياجك


class BookingDetailView(generics.RetrieveDestroyAPIView):
    """عرض وحذف حجز معين"""
    queryset = Booking.objects.all().select_related("student", "group")
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]
