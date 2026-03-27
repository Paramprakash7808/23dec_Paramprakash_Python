"""
Doctor Finder - Models
Practical 7: MVT Pattern - Model layer
Practical 8: Admin Panel - custom fields
Practical 11: Database Connectivity (ORM models map to DB tables)
Practical 12: ORM and QuerySets (CRUD operations)
Practical 15: Customizing Admin Panel (detailed doctor info)
"""

from django.db import models
from django.contrib.auth.models import User


# Practical 7, 11, 12, 15: Doctor model with all fields
class Doctor(models.Model):
    SPECIALITY_CHOICES = [
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('neurologist', 'Neurologist'),
        ('orthopedic', 'Orthopedic'),
        ('pediatrician', 'Pediatrician'),
        ('psychiatrist', 'Psychiatrist'),
        ('general', 'General Physician'),
        ('dentist', 'Dentist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('gynecologist', 'Gynecologist'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('on_leave', 'On Leave'),
    ]

    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=100, choices=SPECIALITY_CHOICES, default='general')
    qualification = models.CharField(max_length=300)
    experience_years = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default='Gujarat')
    # Practical 15: Availability field for admin panel
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    # Practical 20: Google Maps - latitude and longitude for doctor location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    profile_image = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialty_display()}"


# Practical 13: Patient / User profile model for registration & login
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Practical 14 & 16: Appointment model (used in AJAX CRUD and payment)
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    # Practical 16: Paytm transaction ID
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f"{self.patient.username} -> Dr. {self.doctor.name} on {self.appointment_date}"
