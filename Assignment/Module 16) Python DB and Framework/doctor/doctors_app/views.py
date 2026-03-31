from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DoctorProfile, Specialty, PatientProfile, Appointment, SavedDoctor

def home(request):
    """Home page view (Practical 1)"""
    return render(request, 'home.html')

def contact(request):
    """Contact page view (Practical 9)"""
    return render(request, 'contact.html')

from django.db.models import Q

def doctor_list(request):
    """Doctor list view with Search (Practical 7, 9, 21)"""
    query = request.GET.get('q')
    doctors = DoctorProfile.objects.all()
    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) | 
            Q(specialty__name__icontains=query) |
            Q(location_name__icontains=query)
        )
    return render(request, 'doctor_list.html', {'doctors': doctors, 'query': query})

from django.conf import settings

def doctor_profile(request, pk):
    """Doctor profile view (Practical 2, 7, 9, 20)"""
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    saved = False
    if request.user.is_authenticated:
        saved = SavedDoctor.objects.filter(user=request.user, doctor=doctor).exists()
    
    context = {
        'doctor': doctor, 
        'saved': saved,
        'google_maps_api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    }
    return render(request, 'doctor_profile.html', context)

@login_required
def book_appointment(request, pk):
    """View to handle appointment booking and redirect to payment"""
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message', '')
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=request.user,
            date=date,
            time=time,
            message=message,
            status='pending'
        )
        # Redirect to Paytm Payment with appointment ID
        return redirect('paytm_payment', appointment_id=appointment.id)
    return redirect('doctor_profile', pk=pk)

@login_required
def toggle_save_doctor(request, pk):
    """View to toggle saving/unsaving a doctor"""
    doctor = get_object_or_404(DoctorProfile, pk=pk)
    saved_doc, created = SavedDoctor.objects.get_or_create(user=request.user, doctor=doctor)
    if not created:
        saved_doc.delete()
        return JsonResponse({'status': 'unwrapped'})
    return JsonResponse({'status': 'wrapped'})

@login_required
def profile(request):
    """User dashboard view (Practical 13)"""
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date')
    saved_doctors = SavedDoctor.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'appointments': appointments,
        'saved_doctors': saved_doctors
    })

# AJAX CRUD Operations (Practical 14)
def doctor_crud_ajax(request):
    """View to handle AJAX CRUD operations for doctors (Practical 14)"""
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name')
            specialty_id = request.POST.get('specialty')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            
            specialty = Specialty.objects.get(id=specialty_id)
            doctor = DoctorProfile.objects.create(
                name=name,
                specialty=specialty,
                email=email,
                phone=phone
            )
            return JsonResponse({'status': 'success', 'doctor': {'id': doctor.id, 'name': doctor.name}})
            
        elif action == 'delete':
            doctor_id = request.POST.get('id')
            DoctorProfile.objects.filter(id=doctor_id).delete()
            return JsonResponse({'status': 'success'})
            
    doctors = DoctorProfile.objects.all()
    specialties = Specialty.objects.all()
    return render(request, 'doctors_crud.html', {'doctors': doctors, 'specialties': specialties})

# Paytm Integration (Practical 16 - Simplified Functional Simulation)
def paytm_payment(request, appointment_id):
    """Simulated Paytm payment gateway page"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    context = {
        'appointment': appointment,
        'order_id': f'PAYTM_{appointment.id}',
        'amount': '500.00', # Standard consultation fee
        'currency': 'INR',
    }
    return render(request, 'paytm_payment.html', context)

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count

@staff_member_required
def admin_dashboard(request):
    """Admin-only dashboard for managing the platform"""
    total_users = User.objects.filter(is_staff=False).count()
    total_doctors = DoctorProfile.objects.count()
    all_appointments = Appointment.objects.all().order_by('-created_at')
    confirmed_count = Appointment.objects.filter(status='confirmed').count()
    total_revenue = confirmed_count * 500
    
    context = {
        'total_users': total_users,
        'total_doctors': total_doctors,
        'total_revenue': total_revenue,
        'appointments': all_appointments,
        'recent_users': User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def update_appointment_status(request, pk, status):
    """View to approve/reject and simulate notifications (Lab 15, 17)"""
    appointment = get_object_or_404(Appointment, pk=pk)
    if status in ['confirmed', 'cancelled']:
        appointment.status = status
        appointment.save()
        
        # Simulated Notifications (Fulfills Labs 15 & 17)
        if status == 'confirmed':
            print(f"\n--- SIMULATED NOTIFICATION SENT ---")
            print(f"TO: {appointment.patient.email}")
            print(f"EMAIL (Lab 15): Your appointment with Dr. {appointment.doctor.name} on {appointment.date} is CONFIRMED.")
            print(f"SMS (Lab 17): Appointment with Dr. {appointment.doctor.name} confirmed. Order ID: PAYTM_{appointment.id}")
            print(f"--- END OF NOTIFICATION ---\n")
            
    return redirect('admin_dashboard')

@staff_member_required
def admin_user_view(request, user_id):
    """Admin-only view to inspect a specific user's profile and history"""
    user_to_view = get_object_or_404(User, id=user_id)
    appointments = Appointment.objects.filter(patient=user_to_view).order_by('-date')
    return render(request, 'admin_user_profile.html', {
        'target_user': user_to_view,
        'appointments': appointments
    })

def paytm_callback(request, appointment_id):
    """Paytm callback verification and status update"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Simulate payment success
    appointment.status = 'confirmed'
    appointment.save()
    return JsonResponse({'status': 'payment_verified', 'redirect_url': '/profile/'})
