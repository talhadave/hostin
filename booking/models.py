# models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import rooms
from User.models import Student

Choice = (("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected"))


class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(rooms, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now=True)
    description = models.TextField()
    cnic = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default="Pending", choices=Choice)

    def __str__(self):
        return f"{self.student.user.username} - {self.room.room_type}"
