from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.doctor_profile, name='doctor_profile'),
    path('doctors/<int:pk>/book/', views.book_appointment, name='book_appointment'),
    path('doctors/<int:pk>/save/', views.toggle_save_doctor, name='toggle_save_doctor'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('ajax_crud/', views.doctor_crud_ajax, name='doctor_crud_ajax'),
    path('paytm/payment/<int:appointment_id>/', views.paytm_payment, name='paytm_payment'),
    path('paytm/callback/<int:appointment_id>/', views.paytm_callback, name='paytm_callback'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/appointment/<int:pk>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('admin/user/<int:user_id>/', views.admin_user_view, name='admin_user_view'),
]
