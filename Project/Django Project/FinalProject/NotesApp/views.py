from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, NoteForm
from .models import Profile, Note
from django.contrib.auth.decorators import login_required
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
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'NotesApp/index.html', {'notes': notes})

@login_required(login_url='login')
def create_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note created successfully and is pending approval.")
            return redirect('home')
    else:
        form = NoteForm()
    return render(request, 'NotesApp/create_note.html', {'form': form})
