"""
Doctor Finder - Management Command: seed_doctors
Practical 12: ORM and QuerySets - Demonstrate CRUD operations on doctor profiles.
Practical 11: Database Connectivity - inserts records via Django ORM.

Usage:
    python manage.py seed_doctors
"""

from django.core.management.base import BaseCommand
from doctor.models import Doctor


SAMPLE_DOCTORS = [
    {
        'name': 'Rajesh Mehta',
        'specialty': 'cardiologist',
        'qualification': 'MBBS, MD (Cardiology), DM',
        'experience_years': 15,
        'email': 'rajesh.mehta@doctorfinder.com',
        'phone': '9876543210',
        'address': '12, Sarkhej-Gandhinagar Highway, Bodakdev',
        'city': 'Ahmedabad',
        'state': 'Gujarat',
        'availability': 'available',
        'consultation_fee': 800.00,
        'latitude': 23.0549,
        'longitude': 72.5150,
        'bio': 'Senior Cardiologist with 15 years of experience in interventional cardiology.',
    },
    {
        'name': 'Priya Sharma',
        'specialty': 'dermatologist',
        'qualification': 'MBBS, MD (Dermatology)',
        'experience_years': 8,
        'email': 'priya.sharma@doctorfinder.com',
        'phone': '9876543211',
        'address': 'C.G. Road, Navrangpura',
        'city': 'Ahmedabad',
        'state': 'Gujarat',
        'availability': 'available',
        'consultation_fee': 600.00,
        'latitude': 23.0320,
        'longitude': 72.5650,
        'bio': 'Expert in skin care, acne treatment, and cosmetic dermatology.',
    },
    {
        'name': 'Amit Patel',
        'specialty': 'neurologist',
        'qualification': 'MBBS, MD (Neurology), DM',
        'experience_years': 12,
        'email': 'amit.patel@doctorfinder.com',
        'phone': '9876543212',
        'address': 'Shahibaug Road, Near Civil Hospital',
        'city': 'Ahmedabad',
        'state': 'Gujarat',
        'availability': 'busy',
        'consultation_fee': 900.00,
        'latitude': 23.0508,
        'longitude': 72.5905,
        'bio': 'Specialized in epilepsy, stroke, and neurological disorders.',
    },
    {
        'name': 'Sneha Joshi',
        'specialty': 'pediatrician',
        'qualification': 'MBBS, DCH, MD (Paediatrics)',
        'experience_years': 10,
        'email': 'sneha.joshi@doctorfinder.com',
        'phone': '9876543213',
        'address': 'Satellite Road, Jodhpur',
        'city': 'Ahmedabad',
        'state': 'Gujarat',
        'availability': 'available',
        'consultation_fee': 500.00,
        'latitude': 23.0100,
        'longitude': 72.5250,
        'bio': 'Dedicated to child health, growth, and development.',
    },
    {
        'name': 'Vikram Singh',
        'specialty': 'orthopedic',
        'qualification': 'MBBS, MS (Orthopaedics)',
        'experience_years': 18,
        'email': 'vikram.singh@doctorfinder.com',
        'phone': '9876543214',
        'address': 'Drive In Road, Thaltej',
        'city': 'Ahmedabad',
        'state': 'Gujarat',
        'availability': 'available',
        'consultation_fee': 700.00,
        'latitude': 23.0700,
        'longitude': 72.5000,
        'bio': 'Expert in joint replacement, sports injuries, and spine surgery.',
    },
    {
        'name': 'Kavita Desai',
        'specialty': 'gynecologist',
        'qualification': 'MBBS, MS (Obstetrics & Gynaecology)',
        'experience_years': 14,
        'email': 'kavita.desai@doctorfinder.com',
        'phone': '9876543215',
        'address': 'Paldi, Ellis Bridge',
        'city': 'Ahmedabad',
        'state': 'Gujarat',
        'availability': 'available',
        'consultation_fee': 750.00,
        'latitude': 23.0200,
        'longitude': 72.5700,
        'bio': 'Specializes in high-risk pregnancy, infertility, and laparoscopic surgery.',
    },
]


class Command(BaseCommand):
    """
    Practical 12: Management command demonstrating ORM CRUD operations.
    Creates sample doctor records in the database.
    """
    help = (
        'Practical 12: Seed the database with sample doctor records. '
        'Demonstrates Django ORM Create operation.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing doctors before seeding (demonstrates ORM Delete).',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            '\n=== Practical 12: ORM CRUD Demo - seed_doctors ===\n'
        ))

        # ── Practical 12: DELETE (Clear existing records) ───────────
        if options['clear']:
            count = Doctor.objects.count()
            Doctor.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f'[DELETE] Removed {count} existing doctor record(s).'
            ))

        # ── Practical 12: CREATE (Insert sample doctors) ────────────
        created_count = 0
        skipped_count = 0

        for data in SAMPLE_DOCTORS:
            doctor, created = Doctor.objects.get_or_create(
                email=data['email'],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'[CREATE] Added Dr. {doctor.name} ({doctor.get_specialty_display()})'
                ))
            else:
                skipped_count += 1
                self.stdout.write(
                    f'[SKIP]   Dr. {doctor.name} already exists.'
                )

        # ── Practical 12: READ (Query and display all doctors) ──────
        self.stdout.write(self.style.MIGRATE_HEADING('\n[READ] All Doctors in DB (ORM QuerySet):'))
        all_doctors = Doctor.objects.all().order_by('specialty')
        for d in all_doctors:
            self.stdout.write(
                f'  ID={d.id:3d} | {d.name:<20} | {d.get_specialty_display():<20} | '
                f'{d.city:<15} | {d.availability}'
            )

        # ── Practical 12: Filtered QuerySet (Read with filter) ──────
        self.stdout.write(self.style.MIGRATE_HEADING('\n[READ] Available doctors in Ahmedabad:'))
        available = Doctor.objects.filter(city='Ahmedabad', availability='available')
        for d in available:
            self.stdout.write(f'  Dr. {d.name} — {d.get_specialty_display()} — Fee: ₹{d.consultation_fee}')

        # ── Practical 12: UPDATE example ────────────────────────────
        # Update consultation fee for all cardiologists by 10%
        cardio_qs = Doctor.objects.filter(specialty='cardiologist')
        if cardio_qs.exists():
            for d in cardio_qs:
                d.consultation_fee = round(float(d.consultation_fee) * 1.10, 2)
                d.save()
            self.stdout.write(self.style.MIGRATE_HEADING(
                f'\n[UPDATE] Increased consultation fee by 10% for {cardio_qs.count()} cardiologist(s).'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'\n✔ Seeding complete! Created: {created_count}, Skipped: {skipped_count}\n'
            f'  Total doctors in DB: {Doctor.objects.count()}\n'
        ))
        self.stdout.write(
            'Practical 12: CRUD operations demonstrated — Create, Read (all + filtered), Update.\n'
            'To also see Delete: run again with --clear flag.\n'
            '  python manage.py seed_doctors --clear\n'
        )
