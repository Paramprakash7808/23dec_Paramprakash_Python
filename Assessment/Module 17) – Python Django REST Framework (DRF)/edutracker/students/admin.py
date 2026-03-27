"""
Students App – Django Admin Configuration
Registers Student model with custom admin display.
"""

from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'created_at']
    list_filter = ['created_at', 'enrolled_courses']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['enrolled_courses']  # Nice widget for ManyToMany in admin
    ordering = ['last_name', 'first_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Enrolled Courses', {
            'fields': ('enrolled_courses',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
