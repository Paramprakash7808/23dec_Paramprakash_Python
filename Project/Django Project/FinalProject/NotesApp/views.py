from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'NotesApp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'NotesApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home_view(request):
    return render(request, 'NotesApp/index.html')
