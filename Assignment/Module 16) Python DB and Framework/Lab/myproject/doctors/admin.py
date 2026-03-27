from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialty', 'availability', 'is_active')
    list_filter = ('specialty', 'is_active')
    search_fields = ('first_name', 'last_name', 'specialty')
    ordering = ('last_name', 'first_name')
    fieldsets = (
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Professional Info', {
            'fields': ('specialty', 'availability', 'is_active')
        }),
    )
