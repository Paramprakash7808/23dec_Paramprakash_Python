from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Student

# Signup View
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

# Login/Logout are handled directly by Django's built-in views, but we'll use them in URLs

# CRUD Views
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(owner=self.request.user)

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = ['name', 'email', 'course', 'age']
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['name', 'email', 'course', 'age']
    template_name = 'student_form.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('student-list')
