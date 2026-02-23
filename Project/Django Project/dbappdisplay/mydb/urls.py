from django.contrib import admin
from django.urls import path,include
from mydb import views

urlpatterns = [
    path('',views.index),
    path('displaydata/',views.displaydata),
]
