# models.py
from django.contrib.auth.models import User
from django.db import models
from core.models import University

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university_name = models.ForeignKey(University, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True, null=True)   # Add the university_name field
    # Add other student-related fields

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Profile.objects.get_or_create(student=self)


class HostelAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    # Add other hostel admin-related fields

    def __str__(self):
        return self.user.username



class Profile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    # Assuming you're storing profile pictures in a 'profile_pics' directory within your 'MEDIA_ROOT'
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'Profile for user {self.student.user.username}'
