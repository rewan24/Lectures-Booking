from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"  # Include all fields from the Group model

class AddStudentToGroupSerializer(serializers.Serializer):
    student_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False,
        help_text="قائمة بالـ IDs للطلاب"
    )