# models.py
from django.contrib.auth.models import User
from django.db import models
from core.models import University

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university_name = models.ForeignKey(University, on_delete=models.CASCADE)   # Add the university_name field
    # Add other student-related fields

    def __str__(self):
        return self.user.username

class HostelAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Hostel_name = models.CharField(max_length=100) 
    university_name = models.ForeignKey(University, on_delete=models.CASCADE)  # Add the university_name field
    # Add other hostel admin-related fields

    def __str__(self):
        return self.user.username
