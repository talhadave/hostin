from django.db import models
import datetime 
from django.contrib.auth.models import User

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
                return f"{self.name}"
class Hostel(models.Model):
        ownerUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Hostel')
        university = models.ForeignKey(University, on_delete=models.CASCADE)
        hostel_name= models.CharField(max_length=50)
        hostel_adress=models.CharField(max_length=50)
        date=models.DateTimeField("Date Registerd",blank=True,null=True)
        picture = models.ImageField(upload_to='Hostels/', blank=True, null=True)

        def __str__(self):
                return f"{self.hostel_name}{self.hostel_adress}"
        
        
class rooms(models.Model):
      room_number=models.CharField(max_length=30)
      room_number=models.CharField(max_length=30)
      room_price=models.IntegerField()
      hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
      picture = models.ImageField(upload_to='rooms/', blank=True, null=True)
      def __str__(self):
                return f"{self.room_number}{self.room_number}"