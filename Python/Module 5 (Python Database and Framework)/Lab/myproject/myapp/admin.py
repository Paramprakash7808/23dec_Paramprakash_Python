from django.contrib import admin
from .models import Item, Doctor

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    # Organize fields in the detail view
    fieldsets = (
        ('Item Details', {
            'fields': ('title', 'description')
        }),
        ('Ownership & Tracking', {
            'fields': ('user', 'created_at')
        }),
    )

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'email', 'phone', 'user', 'created_at')
    list_filter = ('specialty', 'created_at')
    search_fields = ('name', 'specialty', 'email', 'phone', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Doctor Profile', {
            'fields': ('name', 'specialty', 'email', 'phone')
        }),
        ('Ownership & Tracking', {
            'fields': ('user', 'created_at')
        }),
    )
