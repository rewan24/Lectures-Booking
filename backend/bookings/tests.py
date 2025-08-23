from django.test import TestCase
from django.core.exceptions import ValidationError
from students.models import Student
from groups.models import Group
from bookings.models import Booking


class BookingModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(
            name="Group A",
            capacity=2,
            schedule="Morning",
            days="Saturday, Tuesday"
        )
        self.student1 = Student.objects.create(full_name="Ali Ahmed")
        self.student2 = Student.objects.create(full_name="Sara Mohamed")
        self.student3 = Student.objects.create(full_name="Omar Hassan")

    def test_student_can_book_group(self):
        booking = Booking.objects.create(student=self.student1, group=self.group)
        self.assertEqual(booking.group.students.count(), 1)
        self.assertIn(self.student1, booking.group.students.all())

    def test_student_cannot_book_twice(self):
        Booking.objects.create(student=self.student1, group=self.group)
        with self.assertRaises(Exception):  # IntegrityError or ValidationError
            Booking.objects.create(student=self.student1, group=self.group)

    def test_group_capacity_limit(self):
        Booking.objects.create(student=self.student1, group=self.group)
        Booking.objects.create(student=self.student2, group=self.group)
        with self.assertRaises(ValidationError):
            Booking.objects.create(student=self.student3, group=self.group)
