from django.db import models
from students.models import Student
from groups.models import Group

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="bookings")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="bookings")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="confirmed", choices=(
        ("confirmed", "مؤكد"),
        ("cancelled", "ملغى"),
        ("waiting", "قائمة الانتظار"),
    ))

    class Meta:
        unique_together = ['student', 'group']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} - {self.group.name}"