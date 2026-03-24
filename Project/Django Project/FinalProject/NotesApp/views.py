from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, NoteForm, CategoryForm, ProfileForm, UserUpdateForm
from .models import Profile, Note, Category, UserActivity

def log_activity(user, action, note=None):
    """Helper to create a UserActivity record."""
    UserActivity.objects.create(user=user, action=action, note=note)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
import random

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False # Mark as inactive until OTP verified
            user.save()

            # Create Profile and set OTP
            otp = str(random.randint(100000, 999999))
            phone = form.cleaned_data.get('phone')
            Profile.objects.create(user=user, phone=phone, otp=otp)

            # Send OTP via HTML email
            subject = "Verify Your NotesApp Account"
            recipient_list = [user.email]
            email_from = 'no-reply@notesapp.com'
            
            html_message = render_to_string('NotesApp/emails/otp_email.html', {
                'username': user.username,
                'otp': otp
            })
            
            email = EmailMessage(
                subject,
                html_message,
                email_from,
                recipient_list
            )
            email.content_subtype = "html" # Set to send HTML email
            email.send()

            request.session['verification_user_id'] = user.id
            messages.info(request, "An OTP has been sent to your email. Please verify.")
            return redirect('verify_otp')
    else:
        form = UserRegistrationForm()
    return render(request, 'NotesApp/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'NotesApp/login.html', {'form': form})

def verify_otp_view(request):
    user_id = request.session.get('verification_user_id')
    if not user_id:
        return redirect('register')
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            if profile.otp == entered_otp:
                user.is_active = True
                user.save()
                profile.is_verified = True
                profile.otp = None # Clear OTP once verified
                profile.save()
                messages.success(request, "Email verified successfully! You can now log in.")
                del request.session['verification_user_id']
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        except (User.DoesNotExist, Profile.DoesNotExist):
            messages.error(request, "User session expired or invalid. Please register again.")
            return redirect('register')
            
    return render(request, 'NotesApp/verify_otp.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home_view(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    
    notes = Note.objects.filter(user=request.user, is_archived=False, is_deleted=False)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        notes = notes.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter functionality
    status_filter = request.GET.get('status')
    if status_filter:
        notes = notes.filter(status=status_filter)
        
    category_filter = request.GET.get('category')
    if category_filter:
        notes = notes.filter(category_id=category_filter)
    
    notes = notes.order_by('-is_pinned', '-created_at')
    categories = Category.objects.filter(Q(user=request.user) | Q(user__isnull=True))
    
    return render(request, 'NotesApp/index.html', {
        'notes': notes,
        'categories': categories,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter
    })

@login_required(login_url='login')
def create_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            log_activity(request.user, f"Created note: '{note.title}'", note)
            messages.success(request, "Note created successfully and is pending approval.")
            return redirect('home')
    else:
        form = NoteForm()
        # Filter categories for the current user
        form.fields['category'].queryset = Category.objects.filter(Q(user=request.user) | Q(user__isnull=True))
    return render(request, 'NotesApp/create_note.html', {'form': form})

@login_required(login_url='login')
def edit_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.status = 'Pending' # Reset status for re-approval
            note.save()
            log_activity(request.user, f"Edited note: '{note.title}'", note)
            messages.success(request, "Note updated successfully. It will be re-approved by admin.")
            return redirect('home')
    else:
        form = NoteForm(instance=note)
        form.fields['category'].queryset = Category.objects.filter(Q(user=request.user) | Q(user__isnull=True))
    return render(request, 'NotesApp/edit_note.html', {'form': form, 'note': note})

@login_required(login_url='login')
def delete_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    title = note.title
    note.is_deleted = True
    from django.utils import timezone
    note.deleted_at = timezone.now()
    note.save()
    log_activity(request.user, f"Moved to trash: '{title}'")
    messages.error(request, f"Note '{title}' moved to Trash.")
    return redirect('home')

@login_required(login_url='login')
def toggle_pin_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    status = "pinned" if note.is_pinned else "unpinned"
    log_activity(request.user, f"{'Pinned' if note.is_pinned else 'Unpinned'} note: '{note.title}'", note)
    messages.success(request, f"Note '{note.title}' {status}.")
    return redirect('home')

@login_required(login_url='login')
def manage_categories_view(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Category created successfully.")
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'NotesApp/manage_categories.html', {'categories': categories, 'form': form})

@login_required(login_url='login')
def delete_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    name = category.name
    category.delete()
    messages.error(request, f"Category '{name}' deleted.")
    return redirect('manage_categories')

@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Get or create profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        p_form = ProfileForm(request.POST, request.FILES, instance=profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        profile, created = Profile.objects.get_or_create(user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=profile)

    return render(request, 'NotesApp/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile
    })

@login_required(login_url='login')
def change_password_view(request):
    from .forms import StyledPasswordChangeForm
    if request.method == 'POST':
        form = StyledPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = StyledPasswordChangeForm(request.user)
    return render(request, 'NotesApp/password_change.html', {
        'form': form
    })

@login_required(login_url='login')
def archive_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_archived = True
    note.save()
    log_activity(request.user, f"Archived note: '{note.title}'", note)
    messages.info(request, f"Note '{note.title}' archived.")
    return redirect('home')

@login_required(login_url='login')
def unarchive_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_archived = False
    note.save()
    log_activity(request.user, f"Unarchived note: '{note.title}'", note)
    messages.success(request, f"Note '{note.title}' moved to active notes.")
    return redirect('archive_list')

@login_required(login_url='login')
def archive_list_view(request):
    notes = Note.objects.filter(user=request.user, is_archived=True, is_deleted=False).order_by('-updated_at')
    return render(request, 'NotesApp/archive.html', {'notes': notes})

@login_required(login_url='login')
def trash_view(request):
    notes = Note.objects.filter(user=request.user, is_deleted=True).order_by('-deleted_at')
    return render(request, 'NotesApp/trash.html', {'notes': notes})

@login_required(login_url='login')
def restore_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_deleted = False
    note.deleted_at = None
    note.save()
    log_activity(request.user, f"Restored note from trash: '{note.title}'", note)
    messages.success(request, f"Note '{note.title}' restored.")
    return redirect('trash')

@login_required(login_url='login')
def permanent_delete_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    title = note.title
    note.delete()
    messages.error(request, f"Note '{title}' permanently deleted.")
    return redirect('trash')

@login_required(login_url='login')
def activity_log_view(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:50]
    return render(request, 'NotesApp/activity_log.html', {'activities': activities})

# ── Phase 3: Sharing ───────────────────────────────────────────

@login_required(login_url='login')
def share_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        recipient = User.objects.filter(email=email).first()
        if not recipient:
            messages.error(request, f"No user with email '{email}' found.")
        elif recipient == request.user:
            messages.warning(request, "You can't share a note with yourself.")
        else:
            import uuid as uuid_lib
            if not note.share_token:
                note.share_token = uuid_lib.uuid4()
                note.save()

            link = request.build_absolute_uri(f"/public/{note.share_token}/")
            subject = f"NotesApp — {request.user.username} shared a note with you"
            html_message = f"""
            <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:32px;background:#f8fafc;border-radius:12px;">
                <h2 style="color:#2563eb;">Note Shared With You</h2>
                <p>Hi <strong>{recipient.username}</strong>,</p>
                <p><strong>{request.user.username}</strong> has shared a note titled "<strong>{note.title}</strong>" with you.</p>
                <div style="text-align:center;padding:24px 0;">
                    <a href="{link}" style="display:inline-block;background-color:#2563eb;color:#ffffff;text-decoration:none;padding:12px 24px;border-radius:8px;font-weight:bold;">View Note</a>
                </div>
                <p style="color:#64748b;font-size:12px;">This is a read-only view. Do not share this link if the note is private.</p>
            </div>
            """
            email_obj = EmailMessage(subject, html_message, 'no-reply@notesapp.com', [email])
            email_obj.content_subtype = 'html'
            try:
                email_obj.send()
            except Exception as e:
                pass # Fail silently if SMTP fails

            log_activity(request.user, f"Shared note '{note.title}' with {recipient.username}", note)
            messages.success(request, f"Note shared via email to {recipient.username} successfully!")
        return redirect('share_note', note_id=note.id)
    return render(request, 'NotesApp/share_note.html', {'note': note})

@login_required(login_url='login')
def generate_public_link_view(request, note_id):
    import uuid as uuid_lib
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if not note.share_token:
        note.share_token = uuid_lib.uuid4()
        note.save()
        log_activity(request.user, f"Generated public link for '{note.title}'", note)
        messages.success(request, "Public link generated!")
    else:
        messages.info(request, "Public link already exists for this note.")
    return redirect('share_note', note_id=note.id)

def public_note_view(request, token):
    note = get_object_or_404(Note, share_token=token, is_deleted=False)
    return render(request, 'NotesApp/public_note.html', {'note': note})

# ── Forgot / Reset Password ─────────────────────────────────────

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.filter(email=email, is_active=True).first()
            if not user:
                raise User.DoesNotExist
            profile, _ = Profile.objects.get_or_create(user=user)
            otp = str(random.randint(100000, 999999))
            profile.otp = otp
            profile.save()

            subject = "NotesApp — Password Reset OTP"
            html_message = f"""
            <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:32px;background:#f8fafc;border-radius:12px;">
                <h2 style="color:#2563eb;">Password Reset Request</h2>
                <p>Hi <strong>{user.username}</strong>,</p>
                <p>Use the OTP below to reset your password. It is valid for 10 minutes.</p>
                <div style="text-align:center;padding:24px 0;">
                    <span style="font-size:36px;font-weight:800;letter-spacing:8px;color:#1e293b;background:#e2e8f0;padding:12px 24px;border-radius:8px;">{otp}</span>
                </div>
                <p style="color:#64748b;font-size:12px;">If you didn't request this, ignore this email.</p>
            </div>
            """
            email_obj = EmailMessage(subject, html_message, 'no-reply@notesapp.com', [email])
            email_obj.content_subtype = 'html'
            email_obj.send()

            request.session['reset_user_id'] = user.id
            messages.success(request, "OTP sent to your email. Please check your inbox.")
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, "No active account found with that email.")
    return render(request, 'NotesApp/forgot_password.html')

def reset_password_view(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        new_pass = request.POST.get('password', '')
        confirm_pass = request.POST.get('password2', '')
        try:
            user = User.objects.get(id=user_id)
            profile = Profile.objects.get(user=user)
            if profile.otp != entered_otp:
                messages.error(request, "Invalid OTP. Please try again.")
            elif new_pass != confirm_pass:
                messages.error(request, "Passwords do not match.")
            elif len(new_pass) < 6:
                messages.error(request, "Password must be at least 6 characters.")
            else:
                user.set_password(new_pass)
                user.save()
                profile.otp = None
                profile.save()
                del request.session['reset_user_id']
                messages.success(request, "Password reset successfully! You can now log in.")
                return redirect('login')
        except (User.DoesNotExist, Profile.DoesNotExist):
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot_password')
    return render(request, 'NotesApp/reset_password.html')





