from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
    # Admin management
    path('manage-users/', views.user_management, name='user_management'),
    path('toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
]
