from django.db import models
import datetime 
from django.contrib.auth.models import User

# Create your models here.
class University(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
                return f"{self.name}"
                

class Services(models.Model):
        name = models.CharField(max_length=100)
        def __str__(self):
                return f"{self.name}"
        
class Hostel(models.Model):
        ownerUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Hostels')
        university = models.ForeignKey(University, on_delete=models.CASCADE)
        hostel_name= models.CharField(max_length=50)
        hostel_adress=models.CharField(max_length=50)
        date=models.DateTimeField(auto_now_add=True)
        embedCode = models.TextField(blank=True, null=True)
        picture = models.ImageField(upload_to='Hostels/', blank=True, null=True)
        services = models.ManyToManyField(Services, verbose_name="Services")
        def __str__(self):
                return f"{self.hostel_name}{self.hostel_adress}"

class rooms(models.Model):
      room_type=models.CharField(max_length=30)
      room_price=models.IntegerField()
      hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
      services = models.ManyToManyField(Services, verbose_name="room_Services")
      def __str__(self):
                return f"{self.room_type}{self.room_type}"
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.hostel.hostel_name} - {self.created_at}"

