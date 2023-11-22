# models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import rooms
from User.models import Student

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(rooms, on_delete=models.CASCADE)
    booking_date = models.DateField()
    user_info = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return f"{self.student.user.username} - {self.room.room_type}"
