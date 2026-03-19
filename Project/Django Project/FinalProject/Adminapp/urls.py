from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login_view, name='admin_login'),
    path('', views.admin_dashboard, name='admin_root'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('users/block/<int:user_id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('notes/', views.admin_note_list, name='admin_note_list'),
    path('notes/approve/<int:note_id>/', views.approve_note, name='approve_note'),
    path('notes/reject/<int:note_id>/', views.reject_note, name='reject_note'),
]
