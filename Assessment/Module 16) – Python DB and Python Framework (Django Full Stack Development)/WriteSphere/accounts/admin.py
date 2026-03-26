from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('WriteSphere Info', {
            'fields': ('role', 'bio', 'profile_picture', 'website', 'date_of_birth')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('WriteSphere Info', {
            'fields': ('email', 'role', 'bio', 'profile_picture')
        }),
    )
    actions = ['make_author', 'make_reader']

    def make_author(self, request, queryset):
        queryset.update(role='author')
        self.message_user(request, "Selected users are now Authors.")
    make_author.short_description = "Set role to Author"

    def make_reader(self, request, queryset):
        queryset.update(role='reader')
        self.message_user(request, "Selected users are now Readers.")
    make_reader.short_description = "Set role to Reader"


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    list_filter = ('created_at',)
