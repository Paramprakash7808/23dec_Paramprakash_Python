from django.contrib import admin
from django.urls import path,include
from mydb import views

urlpatterns = [
    path('',views.index),
    path('displaydata/',views.displaydata,name='displaydata'),
    path('update/<int:id>',views.update,name='update'),
    path('deletedata/<int:id>',views.deletedata,name='deletedata'),
]