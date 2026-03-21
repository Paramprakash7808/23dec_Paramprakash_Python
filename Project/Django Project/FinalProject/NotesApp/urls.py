from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('create-note/', views.create_note_view, name='create_note'),
    path('edit-note/<int:note_id>/', views.edit_note_view, name='edit_note'),
    path('delete-note/<int:note_id>/', views.delete_note_view, name='delete_note'),
    path('toggle-pin/<int:note_id>/', views.toggle_pin_view, name='toggle_pin'),
    path('categories/', views.manage_categories_view, name='manage_categories'),
    path('categories/delete/<int:category_id>/', views.delete_category_view, name='delete_category'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
