from rest_framework import serializers
from .models import Booking
from students.models import Student
from groups.models import Group

class BookingSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'student', 'group', 'student_name', 'group_name', 'created_at', 'status']
        read_only_fields = ['created_at', 'status']

    def validate(self, data):
        group = data['group']
        if group.bookings.filter(status="confirmed").count() >= group.capacity:
            raise serializers.ValidationError("المجموعة ممتلئة لا يمكن الحجز")
        
        if Booking.objects.filter(student=data['student'], group=group).exists():
            raise serializers.ValidationError("الطالب محجز في هذه المجموعة مسبقاً")
        
        return data