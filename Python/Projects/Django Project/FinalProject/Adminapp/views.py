from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from NotesApp.models import Note, Profile
from django.contrib import messages
from .models import AuditLog
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse

def is_admin(user):
    return user.is_superuser

def admin_login_view(request):
    return redirect('login')

@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. You do not have administrative privileges.")
        return redirect('home')
    user_count = User.objects.count()
    note_count = Note.objects.count()
    pending_notes = Note.objects.filter(status='Pending').count()
    return render(request, 'Adminapp/dashboard.html', {
        'user_count': user_count,
        'note_count': note_count,
        'pending_notes': pending_notes
    })

@user_passes_test(is_admin, login_url='login')
def admin_user_list(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'Adminapp/user_list.html', {'users': users})

@user_passes_test(is_admin, login_url='login')
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.warning(request, f"User {user.username} has been blocked.")
    return redirect('admin_user_list')

@user_passes_test(is_admin, login_url='login')
def unblock_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"User {user.username} has been unblocked.")
    return redirect('admin_user_list')

@user_passes_test(is_admin, login_url='login')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.error(request, f"User {username} has been deleted.")
    return redirect('admin_user_list')

@user_passes_test(is_admin, login_url='login')
def admin_note_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'Adminapp/note_list.html', {'notes': notes})

@user_passes_test(is_admin, login_url='login')
def approve_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.status = 'Approved'
    note.save()
    
    # Create Audit Log
    AuditLog.objects.create(
        admin=request.user,
        action="Approved Note",
        note=note,
        details=f"Note ID: {note.id}, Title: {note.title}"
    )

    # Send Notification Email
    context = {
        'username': note.user.username,
        'status': 'Approved',
        'note_title': note.title,
        'message': f"Great news! Your note titled '{note.title}' has been approved and is now visible in your dashboard.",
        'status_color': '#10b981', # Green
        'status_bg_color': '#ecfdf5',
        'dashboard_url': request.build_absolute_uri(reverse('home')),
    }
    
    html_message = render_to_string('NotesApp/emails/note_status_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject="Note Approved",
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[note.user.email],
        html_message=html_message,
        fail_silently=True,
    )
    
    messages.success(request, f"Note '{note.title}' approved.")
    return redirect('admin_note_list')

@user_passes_test(is_admin, login_url='login')
def reject_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.status = 'Rejected'
    note.save()
    
    # Create Audit Log
    AuditLog.objects.create(
        admin=request.user,
        action="Rejected Note",
        note=note,
        details=f"Note ID: {note.id}, Title: {note.title}"
    )

    # Send Notification Email
    context = {
        'username': note.user.username,
        'status': 'Rejected',
        'note_title': note.title,
        'message': f"We regret to inform you that your note titled '{note.title}' has been rejected by the admin. Please review our guidelines and try again.",
        'status_color': '#ef4444', # Red
        'status_bg_color': '#fef2f2',
        'dashboard_url': request.build_absolute_uri(reverse('home')),
    }
    
    html_message = render_to_string('NotesApp/emails/note_status_email.html', context)
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject="Note Rejected",
        message=plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[note.user.email],
        html_message=html_message,
        fail_silently=True,
    )
    
    messages.error(request, f"Note '{note.title}' rejected.")
    return redirect('admin_note_list')

@user_passes_test(is_admin, login_url='login')
def audit_log_view(request):
    logs = AuditLog.objects.all().order_by('-timestamp')
    return render(request, 'Adminapp/audit_log.html', {'logs': logs})
