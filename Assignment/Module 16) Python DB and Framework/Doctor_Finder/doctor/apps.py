"""
Practical 6: Django app configuration for the 'doctor' app.
"""

from django.apps import AppConfig


class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor'
    verbose_name = 'Doctor Finder App'

    def ready(self):
        """Practical 13: Import signals for auto profile creation on user registration."""
        import doctor.signals
