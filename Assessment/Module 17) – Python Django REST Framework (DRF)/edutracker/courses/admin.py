"""
Courses App – Django Admin Configuration
"""

from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'instructor', 'duration_weeks', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'instructor', 'description']
    ordering = ['title']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Course Details', {
            'fields': ('title', 'description', 'instructor', 'duration_weeks', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
