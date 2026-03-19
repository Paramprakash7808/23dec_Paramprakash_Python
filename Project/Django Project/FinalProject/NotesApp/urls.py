from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('create-note/', views.create_note_view, name='create_note'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
