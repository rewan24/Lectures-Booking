from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    group_name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "student", "student_name", "group", "group_name", "created_at"]
        read_only_fields = ["created_at"]
