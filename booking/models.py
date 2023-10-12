# models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import rooms

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(rooms, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=10, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.room.room_number}"
