import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_finder.settings')
django.setup()

from doctor.models import Doctor

def add_sample_doctors():
    doctors_data = [
        {
            'name': 'Rajesh Sharma',
            'specialty': 'cardiologist',
            'qualification': 'MBBS, MD (Cardiology)',
            'experience_years': 15,
            'email': 'rajesh@example.com',
            'phone': '9876543210',
            'address': 'Connaught Place',
            'city': 'New Delhi',
            'state': 'Delhi',
            'latitude': 28.6289,
            'longitude': 77.2155,
            'consultation_fee': 800,
            'availability': 'available'
        },
        {
            'name': 'Priya Patel',
            'specialty': 'dermatologist',
            'qualification': 'MBBS, DVD',
            'experience_years': 8,
            'email': 'priya@example.com',
            'phone': '9876543211',
            'address': 'Satellite Area',
            'city': 'Ahmedabad',
            'state': 'Gujarat',
            'latitude': 23.0225,
            'longitude': 72.5714,
            'consultation_fee': 600,
            'availability': 'available'
        },
        {
            'name': 'Amit Verma',
            'specialty': 'neurologist',
            'qualification': 'MBBS, DM (Neurology)',
            'experience_years': 12,
            'email': 'amit@example.com',
            'phone': '9876543212',
            'address': 'Bandra West',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'latitude': 19.0596,
            'longitude': 72.8295,
            'consultation_fee': 1000,
            'availability': 'busy'
        },
        {
            'name': 'Sunita Reddy',
            'specialty': 'pediatrician',
            'qualification': 'MBBS, DCH',
            'experience_years': 10,
            'email': 'sunita@example.com',
            'phone': '9876543213',
            'address': 'Hitech City',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'latitude': 17.4483,
            'longitude': 78.3915,
            'consultation_fee': 500,
            'availability': 'available'
        }
    ]

    for data in doctors_data:
        doctor, created = Doctor.objects.get_or_create(
            email=data['email'],
            defaults=data
        )
        if created:
            print(f"Created Dr. {doctor.name}")
        else:
            # Update existing if email matches but no lat/lng
            if doctor.latitude is None:
                doctor.latitude = data['latitude']
                doctor.longitude = data['longitude']
                doctor.save()
                print(f"Updated Dr. {doctor.name} with coordinates")
            else:
                print(f"Dr. {doctor.name} already exists with coordinates")

if __name__ == "__main__":
    add_sample_doctors()
