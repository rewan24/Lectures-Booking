from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking


@receiver(post_save, sender=Booking)
def add_student_to_group(sender, instance, created, **kwargs):
    """لما يتعمل حجز جديد نضيف الطالب للمجموعة تلقائي"""
    if created:
        instance.group.students.add(instance.student)
