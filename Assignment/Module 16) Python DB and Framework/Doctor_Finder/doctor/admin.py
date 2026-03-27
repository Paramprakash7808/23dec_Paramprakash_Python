"""
Doctor Finder - Admin Panel Configuration
Practical 8: Set up and customize the Django admin panel
Practical 15: Customizing admin to display detailed doctor information
             (specialties, availability, etc.)
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, PatientProfile, Appointment


# Practical 8 & 15: Custom Doctor Admin with all detailed fields
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Practical 15: Display more columns in list view
    list_display = [
        'profile_image_tag', 'name', 'specialty', 'qualification',
        'experience_years', 'phone', 'city', 'availability',
        'consultation_fee', 'created_at'
    ]
    # Practical 15: Filter by specialty and availability
    list_filter = ['specialty', 'availability', 'city', 'state']
    # Practical 15: Search by name, specialty, city
    search_fields = ['name', 'specialty', 'city', 'email', 'phone']
    # Practical 15: Allow inline editing of availability from list view
    list_editable = ['availability', 'consultation_fee']
    # Practical 8: Custom fieldsets for organized display
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'qualification', 'experience_years', 'bio', 'profile_image')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'state')
        }),
        ('Professional Details', {
            'fields': ('specialty', 'availability', 'consultation_fee')
        }),
        ('Location (Google Maps)', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',),
            'description': 'Set latitude and longitude for Google Maps display.'
        }),
    )
    readonly_fields = ['created_at', 'updated_at', 'profile_image_tag']
    ordering = ['name']

    # Practical 15: Show profile image thumbnail in admin list
    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%; object-fit:cover;" />',
                obj.profile_image.url
            )
        return format_html('<span style="color:#999;">No Image</span>')
    profile_image_tag.short_description = 'Photo'

    # Practical 15: Custom actions
    actions = ['mark_available', 'mark_on_leave']

    def mark_available(self, request, queryset):
        queryset.update(availability='available')
        self.message_user(request, "Selected doctors marked as Available.")
    mark_available.short_description = "Mark selected doctors as Available"

    def mark_on_leave(self, request, queryset):
        queryset.update(availability='on_leave')
        self.message_user(request, "Selected doctors marked as On Leave.")
    mark_on_leave.short_description = "Mark selected doctors as On Leave"


# Practical 8 & 13: Patient Profile Admin
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['date_of_birth']


# Practical 8 & 14: Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'patient', 'doctor', 'appointment_date',
        'appointment_time', 'status', 'payment_status', 'amount_paid'
    ]
    list_filter = ['status', 'payment_status', 'appointment_date']
    search_fields = ['patient__username', 'doctor__name', 'transaction_id']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['created_at', 'transaction_id']
    date_hierarchy = 'appointment_date'


# Practical 8: Customize Admin Site Header & Title
admin.site.site_header = "Doctor Finder Administration"
admin.site.site_title = "Doctor Finder Admin"
admin.site.index_title = "Welcome to Doctor Finder Admin Panel"
