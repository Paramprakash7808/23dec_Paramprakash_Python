from django.urls import path
from . import views

urlpatterns = [
    path('pay/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.callback, name='callback'),
]
