from django.urls import path
from django.contrib.auth import views as auth_views
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Password Reset paths
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # AJAX CRUD paths
    path('items/', views.items_page, name='items_page'),
    path('ajax/items/list/', views.list_items, name='list_items'),
    path('ajax/items/create/', views.create_item, name='create_item'),
    path('ajax/items/update/<int:item_id>/', views.update_item, name='update_item'),
    path('ajax/items/delete/<int:item_id>/', views.delete_item, name='delete_item'),

    # Doctor AJAX CRUD paths
    path('doctors/', views.doctors_page, name='doctors_page'),
    path('ajax/doctors/list/', views.list_doctors, name='list_doctors'),
    path('ajax/doctors/create/', views.create_doctor, name='create_doctor'),
    path('ajax/doctors/update/<int:doc_id>/', views.update_doctor, name='update_doctor'),
    path('ajax/doctors/delete/<int:doc_id>/', views.delete_doctor, name='delete_doctor'),
]