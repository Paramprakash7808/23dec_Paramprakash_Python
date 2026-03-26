from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

from django.http import JsonResponse
import json
from .models import Item
from django.views.decorators.csrf import csrf_exempt

@login_required
def items_page(request):
    return render(request, 'items.html')

@login_required
def list_items(request):
    items = Item.objects.filter(user=request.user).order_by('-created_at')
    data = [{'id': item.id, 'title': item.title, 'description': item.description} for item in items]
    return JsonResponse({'items': data})

@login_required
def create_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item = Item.objects.create(
                user=request.user,
                title=data.get('title'),
                description=data.get('description', '')
            )
            return JsonResponse({'success': True, 'item': {'id': item.id, 'title': item.title, 'description': item.description}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def update_item(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=item_id, user=request.user)
            data = json.loads(request.body)
            item.title = data.get('title', item.title)
            item.description = data.get('description', item.description)
            item.save()
            return JsonResponse({'success': True, 'item': {'id': item.id, 'title': item.title, 'description': item.description}})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_item(request, item_id):
    if request.method == 'POST':
        try:
            item = Item.objects.get(id=item_id, user=request.user)
            item.delete()
            return JsonResponse({'success': True})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from .models import Doctor

@login_required
def doctors_page(request):
    return render(request, 'doctors.html')

@login_required
def list_doctors(request):
    doctors = Doctor.objects.filter(user=request.user).order_by('-created_at')
    data = [{'id': doc.id, 'name': doc.name, 'specialty': doc.specialty, 'email': doc.email, 'phone': doc.phone} for doc in doctors]
    return JsonResponse({'doctors': data})

@login_required
def create_doctor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            doc = Doctor.objects.create(
                user=request.user,
                name=data.get('name'),
                specialty=data.get('specialty'),
                email=data.get('email', ''),
                phone=data.get('phone', '')
            )
            return JsonResponse({'success': True, 'doctor': {'id': doc.id, 'name': doc.name, 'specialty': doc.specialty, 'email': doc.email, 'phone': doc.phone}})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def update_doctor(request, doc_id):
    if request.method == 'POST':
        try:
            doc = Doctor.objects.get(id=doc_id, user=request.user)
            data = json.loads(request.body)
            doc.name = data.get('name', doc.name)
            doc.specialty = data.get('specialty', doc.specialty)
            doc.email = data.get('email', doc.email)
            doc.phone = data.get('phone', doc.phone)
            doc.save()
            return JsonResponse({'success': True, 'doctor': {'id': doc.id, 'name': doc.name, 'specialty': doc.specialty, 'email': doc.email, 'phone': doc.phone}})
        except Doctor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doctor not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def delete_doctor(request, doc_id):
    if request.method == 'POST':
        try:
            doc = Doctor.objects.get(id=doc_id, user=request.user)
            doc.delete()
            return JsonResponse({'success': True})
        except Doctor.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Doctor not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
