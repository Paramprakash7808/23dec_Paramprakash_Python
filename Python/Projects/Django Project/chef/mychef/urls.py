from django.contrib import admin
from django.urls import path,include
from mychef import views

urlpatterns = [
    path('',views.index),
]