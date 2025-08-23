# backend/bookings/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Booking(models.Model):
    """ نموذج الحجز بين الطالب والمجموعة """
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "group")  # نفس الطالب ما يحجزش مرتين في نفس المجموعة
        ordering = ["-created_at"]

    def clean(self):
        """ تحقق إن المجموعة فيها أماكن قبل الحجز """
        if self.group.students.count() >= self.group.capacity:
            raise ValidationError("المجموعة ممتلئة ولا يمكن الحجز فيها")

    def __str__(self):
        """ اسم الطالب واسم المجموعة """
        return f"{self.student.full_name} حجز في {self.group.name}"
