"""
Doctor Finder - Views
Practical 1:  Render HTML file using Django template system
Practical 2:  CSS styled doctor profile page
Practical 3:  JavaScript form validation view
Practical 7:  MVT Pattern - View layer
Practical 9:  URL routing - home, profile, contact pages
Practical 12: ORM CRUD operations on doctor profiles
Practical 13: User sign up, login, password reset, profile update
Practical 14: AJAX CRUD operations (add/edit/delete without page refresh)
Practical 16: Paytm payment integration
Practical 19: Social auth handled by social_django (no custom view needed)
Practical 20: Google Maps API - display doctor locations
"""

import json
import hashlib
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm

from .models import Doctor, PatientProfile, Appointment
from .forms import (
    PatientRegistrationForm, PatientLoginForm,
    PatientProfileUpdateForm, DoctorForm, AppointmentForm
)


# ─────────────────────────────────────────────
# Practical 1 & 9: HOME PAGE - renders HTML template
# ─────────────────────────────────────────────
def home(request):
    """
    Practical 1: Render an HTML file using Django's template system.
    Displays 'Welcome to Doctor Finder' on the home page.
    Practical 9: Home page URL routing.
    """
    doctors = Doctor.objects.filter(availability='available')[:6]
    context = {
        'page_title': 'Welcome to Doctor Finder',
        'doctors': doctors,
    }
    return render(request, 'doctor/home.html', context)


# ─────────────────────────────────────────────
# Practical 2 & 9: DOCTOR PROFILE PAGE with CSS styling
# ─────────────────────────────────────────────
def doctor_profile(request, pk):
    """
    Practical 2: Display doctor profile page with custom CSS styling.
    Practical 9: Profile URL routing.
    """
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {'doctor': doctor}
    return render(request, 'doctor/profile.html', context)


# ─────────────────────────────────────────────
# Practical 9: CONTACT PAGE
# ─────────────────────────────────────────────
def contact(request):
    """Practical 9: Contact page URL routing."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f"Thank you {name}! Your message has been received.")
        return redirect('contact')
    return render(request, 'doctor/contact.html', {'page_title': 'Contact Us'})


# ─────────────────────────────────────────────
# Practical 12: CRUD - List all doctors
# ─────────────────────────────────────────────
def doctor_list(request):
    """
    Practical 12: Read operation - List all doctor profiles using Django ORM.
    """
    specialty = request.GET.get('specialty', '')
    city = request.GET.get('city', '')

    # Practical 12: ORM QuerySet with filtering
    doctors = Doctor.objects.all()
    if specialty:
        doctors = doctors.filter(specialty=specialty)
    if city:
        doctors = doctors.filter(city__icontains=city)

    specialties = Doctor.SPECIALITY_CHOICES
    context = {
        'doctors': doctors,
        'specialties': specialties,
        'selected_specialty': specialty,
        'selected_city': city,
    }
    return render(request, 'doctor/doctor_list.html', context)


# ─────────────────────────────────────────────
# Practical 13: USER REGISTRATION
# ─────────────────────────────────────────────
def register(request):
    """
    Practical 13: User sign up with form validation.
    Practical 3 & 10: JavaScript validates fields client-side first.
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            # Create patient profile
            PatientProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone']
            )
            login(request, user)
            messages.success(request, f"Account created! Welcome {user.first_name}!")
            return redirect('home')
    else:
        form = PatientRegistrationForm()
    return render(request, 'registration/register.html', {'form': form, 'page_title': 'Patient Registration'})


# ─────────────────────────────────────────────
# Practical 13: LOGIN
# ─────────────────────────────────────────────
def user_login(request):
    """Practical 13: User login."""
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = PatientLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(request.GET.get('next', 'home'))
    else:
        form = PatientLoginForm()
    return render(request, 'registration/login.html', {'form': form, 'page_title': 'Login'})


# ─────────────────────────────────────────────
# Practical 13: LOGOUT
# ─────────────────────────────────────────────
def user_logout(request):
    """Practical 13: User logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ─────────────────────────────────────────────
# Practical 13: PROFILE UPDATE
# ─────────────────────────────────────────────
@login_required
def profile_update(request):
    """Practical 13: Update user profile."""
    try:
        patient_profile = request.user.patient_profile
    except PatientProfile.DoesNotExist:
        patient_profile = PatientProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = PatientProfileUpdateForm(request.POST, request.FILES, instance=patient_profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_update')
    else:
        form = PatientProfileUpdateForm(
            instance=patient_profile,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        )
    return render(request, 'registration/profile.html', {'form': form, 'page_title': 'My Profile'})


# ─────────────────────────────────────────────
# Practical 13: PASSWORD RESET
# ─────────────────────────────────────────────
@login_required
def change_password(request):
    """Practical 13: Password reset/change."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect('profile_update')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


# ─────────────────────────────────────────────
# Practical 12 & 14: AJAX CRUD - List doctors as JSON
# ─────────────────────────────────────────────
def ajax_doctor_list(request):
    """
    Practical 14: Return all doctor profiles as JSON for AJAX.
    Practical 12: Read operation using ORM.
    """
    doctors = Doctor.objects.all().values(
        'id', 'name', 'specialty', 'qualification', 'experience_years',
        'email', 'phone', 'city', 'availability', 'consultation_fee'
    )
    return JsonResponse({'doctors': list(doctors)})


# ─────────────────────────────────────────────
# Practical 14: AJAX - ADD doctor (Create)
# ─────────────────────────────────────────────
@require_POST
def ajax_add_doctor(request):
    """
    Practical 14: AJAX Create - Add a doctor profile without page refresh.
    Practical 12: Create operation using Django ORM.
    """
    try:
        data = json.loads(request.body)
        doctor = Doctor.objects.create(
            name=data['name'],
            specialty=data['specialty'],
            qualification=data['qualification'],
            experience_years=int(data.get('experience_years', 0)),
            email=data['email'],
            phone=data['phone'],
            address=data.get('address', ''),
            city=data.get('city', ''),
            state=data.get('state', 'Gujarat'),
            consultation_fee=float(data.get('consultation_fee', 500)),
            availability=data.get('availability', 'available'),
        )
        return JsonResponse({
            'success': True,
            'message': f'Dr. {doctor.name} added successfully!',
            'doctor': {
                'id': doctor.id,
                'name': doctor.name,
                'specialty': doctor.get_specialty_display(),
                'city': doctor.city,
                'availability': doctor.availability,
                'consultation_fee': str(doctor.consultation_fee),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ─────────────────────────────────────────────
# Practical 14: AJAX - GET single doctor for editing
# ─────────────────────────────────────────────
def ajax_get_doctor(request, pk):
    """Practical 14: AJAX - Get single doctor details for edit modal."""
    doctor = get_object_or_404(Doctor, pk=pk)
    return JsonResponse({
        'id': doctor.id,
        'name': doctor.name,
        'specialty': doctor.specialty,
        'qualification': doctor.qualification,
        'experience_years': doctor.experience_years,
        'email': doctor.email,
        'phone': doctor.phone,
        'address': doctor.address,
        'city': doctor.city,
        'state': doctor.state,
        'consultation_fee': str(doctor.consultation_fee),
        'availability': doctor.availability,
    })


# ─────────────────────────────────────────────
# Practical 14: AJAX - EDIT doctor (Update)
# ─────────────────────────────────────────────
@require_http_methods(["PUT", "POST"])
def ajax_edit_doctor(request, pk):
    """
    Practical 14: AJAX Update - Edit doctor profile without page refresh.
    Practical 12: Update operation using Django ORM.
    """
    doctor = get_object_or_404(Doctor, pk=pk)
    try:
        data = json.loads(request.body)
        doctor.name = data.get('name', doctor.name)
        doctor.specialty = data.get('specialty', doctor.specialty)
        doctor.qualification = data.get('qualification', doctor.qualification)
        doctor.experience_years = int(data.get('experience_years', doctor.experience_years))
        doctor.email = data.get('email', doctor.email)
        doctor.phone = data.get('phone', doctor.phone)
        doctor.address = data.get('address', doctor.address)
        doctor.city = data.get('city', doctor.city)
        doctor.state = data.get('state', doctor.state)
        doctor.consultation_fee = float(data.get('consultation_fee', doctor.consultation_fee))
        doctor.availability = data.get('availability', doctor.availability)
        doctor.save()
        return JsonResponse({
            'success': True,
            'message': f'Dr. {doctor.name} updated successfully!'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ─────────────────────────────────────────────
# Practical 14: AJAX - DELETE doctor
# ─────────────────────────────────────────────
@require_http_methods(["DELETE", "POST"])
def ajax_delete_doctor(request, pk):
    """
    Practical 14: AJAX Delete - Delete doctor profile without page refresh.
    Practical 12: Delete operation using Django ORM.
    """
    doctor = get_object_or_404(Doctor, pk=pk)
    name = doctor.name
    doctor.delete()
    return JsonResponse({'success': True, 'message': f'Dr. {name} deleted successfully!'})


# ─────────────────────────────────────────────
# Practical 14: AJAX CRUD Management Page
# ─────────────────────────────────────────────
@login_required
def ajax_crud_page(request):
    """
    Practical 14: Page that uses AJAX to add/edit/delete doctor profiles
    without refreshing the page.
    """
    return render(request, 'doctor/ajax_crud.html', {'page_title': 'Manage Doctors (AJAX)'})


# ─────────────────────────────────────────────
# Practical 16: PAYTM PAYMENT INTEGRATION
# ─────────────────────────────────────────────
@login_required
def initiate_payment(request, appointment_id):
    """
    Practical 16: Initiate Paytm payment for an appointment.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    amount = str(appointment.doctor.consultation_fee)
    order_id = f"ORDER_{appointment.id}_{request.user.id}"

    # Paytm parameters
    paytm_params = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'ORDER_ID': order_id,
        'CUST_ID': str(request.user.id),
        'TXN_AMOUNT': amount,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'CALLBACK_URL': request.build_absolute_uri(f'/payment/callback/{appointment_id}/'),
        'EMAIL': request.user.email,
        'MOBILE_NO': getattr(request.user, 'patient_profile', None) and request.user.patient_profile.phone or '',
    }

    # Practical 16: Generate Paytm checksum using paytmchecksum library
    try:
        import paytmchecksum
        checksum = paytmchecksum.generateSignature(paytm_params, settings.PAYTM_MERCHANT_KEY)
    except (ImportError, ValueError):
        # Fallback for development/demo if library not installed OR key is invalid length (AES error)
        checksum = "DEMO_CHECKSUM_FOR_DEVELOPMENT"

    paytm_params['CHECKSUMHASH'] = checksum

    context = {
        'paytm_params': paytm_params,
        'paytm_url': settings.PAYTM_TRANSACTION_URL,
        'appointment': appointment,
        'page_title': 'Payment',
    }
    return render(request, 'doctor/payment.html', context)


@csrf_exempt
def payment_callback(request, appointment_id):
    """
    Practical 16: Paytm payment callback - handle payment response.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        paytm_response = request.POST.dict()
        txn_id = paytm_response.get('TXNID', '')
        status = paytm_response.get('STATUS', '')
        amount = paytm_response.get('TXNAMOUNT', '0')

        if status == 'TXN_SUCCESS':
            appointment.payment_status = 'paid'
            appointment.transaction_id = txn_id
            appointment.amount_paid = float(amount)
            appointment.status = 'confirmed'
            appointment.save()
            messages.success(request, f"Payment successful! Transaction ID: {txn_id}")
        else:
            messages.error(request, "Payment failed. Please try again.")

    return redirect('home')


# ─────────────────────────────────────────────
# Appointment Booking
# ─────────────────────────────────────────────
@login_required
def book_appointment(request):
    """Book appointment - leads to Paytm payment (Practical 16)."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, "Appointment booked! Proceed to payment.")
            return redirect('initiate_payment', appointment_id=appointment.id)
    else:
        doctor_id = request.GET.get('doctor')
        initial = {'doctor': doctor_id} if doctor_id else {}
        form = AppointmentForm(initial=initial)
    return render(request, 'doctor/book_appointment.html', {'form': form, 'page_title': 'Book Appointment'})


# ─────────────────────────────────────────────
# Practical 20: GOOGLE MAPS - Display doctor locations
# ─────────────────────────────────────────────
def doctor_map(request):
    """
    Practical 20: Display doctor locations using Google Maps API.
    """
    doctors = Doctor.objects.exclude(latitude=None).exclude(longitude=None)
    doctors_list = [
        {
            'id': d.id,
            'name': f"Dr. {d.name}",
            'specialty': d.get_specialty_display(),
            'address': d.address,
            'city': d.city,
            'phone': d.phone,
            'availability': d.availability,
            'lat': float(d.latitude),
            'lng': float(d.longitude),
        }
        for d in doctors
    ]
    context = {
        'doctors_list': doctors_list,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'page_title': 'Doctor Locations Map',
    }
    return render(request, 'doctor/doctor_map.html', context)
