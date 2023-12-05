from django.db import models
import datetime
from django.contrib.auth.models import User


# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"




FIRST_CHOICE = "For Boys"
SECOND_CHOICE = "For Girls "
THIRD_CHOICE = "Both for Boys and Girls"

MY_CHOICES = [
    (FIRST_CHOICE, "For Boys"),
    (SECOND_CHOICE, "For Girls "),
    (THIRD_CHOICE, "Both for Boys and Girls"),
]


class Hostel(models.Model):
    ownerUser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Hostels"
    )
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    hostel_name = models.CharField(max_length=50)
    hostel_adress = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    embedCode = models.TextField(blank=False, null=True)
    picture = models.ImageField(upload_to="Hostels/", blank=True, null=True)
    services = models.TextField(blank=True)

    hostel_type = models.CharField(
        max_length=50,
        choices=MY_CHOICES,
        default=FIRST_CHOICE,
    )

    def __str__(self):
        return f"{self.hostel_name}"


class rooms(models.Model):
    room_price = models.IntegerField()
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="room")
    services = models.TextField(blank=True)
    floor = models.CharField(max_length=20)
    picture = models.ImageField(upload_to="Rooms/", blank=True, null=True)
    FIRST_CHOICE = "Two Seated"
    SECOND_CHOICE = "Three Seated "
    THIRD_CHOICE = "Four Seated"
    FOURTH_CHOICE = "Five Seated"

    MY_CHOICES = [
        (FIRST_CHOICE, "Two Seated"),
        (SECOND_CHOICE, "Three Seated "),
        (THIRD_CHOICE, "Four Seated"),
        (FOURTH_CHOICE, "Five Seated"),
    ]

    room_type = models.CharField(
        max_length=30,
        choices=MY_CHOICES,
        default=FIRST_CHOICE,
    )

    def __str__(self):
        return f"{self.room_type}"


