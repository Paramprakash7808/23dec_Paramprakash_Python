from django.contrib import admin
from django.urls import path,include
from mychef import views

urlpatterns = [
    path('',views.index),
    path('about/',views.about),
    path('blog/',views.blog),
    path('contact/',views.contact),
    path('menu/',views.menu),
    path('team/',views.team),
    path('testimonial/',views.testimonial),
]