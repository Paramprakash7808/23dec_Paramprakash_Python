from django.contrib import admin
from django.urls import path,include
from myaiTech import views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('contact/',views.contact),
    path('project/',views.project),
    path('service/',views.service),
]