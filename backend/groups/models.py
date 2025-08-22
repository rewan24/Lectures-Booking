from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    schedule = models.CharField(max_length=100)
    students = models.ManyToManyField("students.Student", blank=True, related_name="groups")
    days = models.CharField(max_length=100, blank=True, help_text="اكتب مواعيد المجموعة مثل: سبت، تلات")

    def __str__(self):
        return f"{self.name} - {self.schedule} - {self.days}"
