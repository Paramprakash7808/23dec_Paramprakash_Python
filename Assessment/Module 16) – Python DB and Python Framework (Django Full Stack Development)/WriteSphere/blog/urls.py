from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('posts/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('posts/<slug:slug>/delete/', views.post_delete, name='post_delete'),
    path('posts/<slug:slug>/like/', views.like_toggle, name='like_toggle'),
    path('comments/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<str:tag>/', views.tag_posts, name='tag_posts'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
