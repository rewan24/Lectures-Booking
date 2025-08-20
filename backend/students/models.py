from django.db import models
from django.utils import timezone
from django.db.models.functions import Lower

STAGE_CHOICES = (
    ("GRADE6", "سادس ابتدائي"),
    ("PREP", "إعدادي"),
)

class Student(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=15, unique=True)  # صيغة مصر هنفحصها في الـ serializer
    birth_date = models.DateField(null=True, blank=True)
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES)
    notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(Lower("email"), name="idx_student_email_ci"),
            models.Index(models.F("phone"), name="idx_student_phone"),
        ]
        constraints = [
            models.UniqueConstraint(Lower("email"), name="unique_student_email_ci"),
        ]
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower().strip()
        if self.full_name:
            self.full_name = " ".join(self.full_name.split())
        super().save(*args, **kwargs)

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = timezone.now().date()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    def __str__(self):
        return f"{self.full_name} ({self.get_stage_display()})"
