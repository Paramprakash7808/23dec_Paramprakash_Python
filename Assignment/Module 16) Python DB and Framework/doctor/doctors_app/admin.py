from django.contrib import admin
from .models import Specialty, DoctorProfile, PatientProfile

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'phone', 'email', 'experience_years', 'availability')
    list_filter = ('specialty', 'availability')
    search_fields = ('name', 'specialty__name', 'phone', 'email')
    ordering = ('name',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'specialty', 'profile_pic', 'bio', 'experience_years')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone')
        }),
        ('Work Details', {
            'fields': ('availability', 'location_name', 'latitude', 'longitude')
        }),
    )

@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'date_of_birth')
    search_fields = ('user__username', 'phone')
