"""
Doctor Finder - Main URL Configuration
Practical 9: URL Patterns and Template Integration
Practical 13: Authentication URLs (sign up, login, password reset, profile update)
Practical 16: Payment URLs
Practical 19: Social Authentication URLs
Practical 20: Google Maps URL
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Practical 8 & 15: Django Admin Panel
    path('admin/', admin.site.urls),

    # Practical 9: Doctor app URLs (home, profile, contact)
    path('', include('doctor.urls')),

    # Practical 19: Social Authentication URLs (Google & Facebook login)
    path('social-auth/', include('social_django.urls', namespace='social')),

    # ── Practical 13: Password Reset URLs (for unauthenticated users) ────────
    # Step 1: User submits email  → sends reset link
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt',
         ),
         name='password_reset'),

    # Step 2: Confirmation page shown after email is sent
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    # Step 3: User clicks link in email → enters new password
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    # Step 4: Success page after password has been reset
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
