from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, Profile

@receiver(post_save, sender=Student)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(student=instance)
    else:
        instance.profile.save()  # Save the profile if it already exists