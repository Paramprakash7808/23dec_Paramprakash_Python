"""
Doctor Finder - Signals
Practical 13: Auto-create PatientProfile when a new User registers.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import PatientProfile


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Practical 13: Automatically create a PatientProfile
    whenever a new User account is created.
    """
    if created:
        PatientProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    """Practical 13: Save PatientProfile whenever the User is saved."""
    try:
        instance.patient_profile.save()
    except PatientProfile.DoesNotExist:
        PatientProfile.objects.create(user=instance)
