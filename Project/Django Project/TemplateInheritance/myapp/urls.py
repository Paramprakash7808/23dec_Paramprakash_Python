from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.base),
    path('base/', views.base),
    path('home/', views.home),
    path('about/', views.about),
    path('contact/', views.contact)
]