"""
Doctor Finder - URL Patterns
Practical 9: URL routing to navigate between pages (home, profile, contact)
Practical 13: Authentication URLs
Practical 14: AJAX CRUD URLs
Practical 16: Payment URLs
Practical 20: Google Maps URL
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Practical 1 & 9: Home Page ──────────────────────────────
    path('', views.home, name='home'),

    # ── Practical 9: Doctor pages ────────────────────────────────
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:pk>/', views.doctor_profile, name='doctor_profile'),
    path('contact/', views.contact, name='contact'),

    # ── Practical 13: Authentication URLs ────────────────────────
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_update, name='profile_update'),
    path('change-password/', views.change_password, name='change_password'),

    # ── Practical 14: AJAX CRUD URLs ─────────────────────────────
    path('manage-doctors/', views.ajax_crud_page, name='ajax_crud_page'),
    path('ajax/doctors/', views.ajax_doctor_list, name='ajax_doctor_list'),
    path('ajax/doctors/add/', views.ajax_add_doctor, name='ajax_add_doctor'),
    path('ajax/doctors/<int:pk>/', views.ajax_get_doctor, name='ajax_get_doctor'),
    path('ajax/doctors/<int:pk>/edit/', views.ajax_edit_doctor, name='ajax_edit_doctor'),
    path('ajax/doctors/<int:pk>/delete/', views.ajax_delete_doctor, name='ajax_delete_doctor'),

    # ── Appointment booking ──────────────────────────────────────
    path('book-appointment/', views.book_appointment, name='book_appointment'),

    # ── Practical 16: Paytm Payment URLs ─────────────────────────
    path('payment/<int:appointment_id>/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/<int:appointment_id>/', views.payment_callback, name='payment_callback'),

    # ── Practical 20: Google Maps URL ────────────────────────────
    path('map/', views.doctor_map, name='doctor_map'),
]
