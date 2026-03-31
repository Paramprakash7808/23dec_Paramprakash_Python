import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor.settings')
django.setup()

from doctors_app.models import Specialty, DoctorProfile
from django.contrib.auth.models import User

def populate():
    # Create Specialties
    cardiology, _ = Specialty.objects.get_or_create(name='Cardiology')
    neurology, _ = Specialty.objects.get_or_create(name='Neurology')
    pediatrics, _ = Specialty.objects.get_or_create(name='Pediatrics')
    dermatology, _ = Specialty.objects.get_or_create(name='Dermatology')

    # Create Doctors
    DoctorProfile.objects.get_or_create(
        name='Aarav Sharma',
        specialty=cardiology,
        email='aarav.sharma@example.com',
        phone='9876543210',
        bio='Dr. Aarav is a world-renowned cardiologist with over 15 years of experience in treating complex heart conditions.',
        experience_years=15,
        availability='Mon-Fri, 10am-4pm',
        location_name='Mumbai Heart Center'
    )

    DoctorProfile.objects.get_or_create(
        name='Ishani Gupta',
        specialty=neurology,
        email='ishani.gupta@example.com',
        phone='8765432109',
        bio='Dr. Ishani specializes in neurological disorders and brain surgeries, providing compassionate care to her patients.',
        experience_years=12,
        availability='Tue-Sat, 11am-5pm',
        location_name='Delhi Neuro Clinic'
    )

    DoctorProfile.objects.get_or_create(
        name='Vikram Singh',
        specialty=pediatrics,
        email='vikram.singh@example.com',
        phone='7654321098',
        bio='Dr. Vikram is dedicated to the health and well-being of children, from infants to adolescents.',
        experience_years=10,
        availability='Mon-Wed-Fri, 9am-2pm',
        location_name='Bangalore Kids Hospital'
    )

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
