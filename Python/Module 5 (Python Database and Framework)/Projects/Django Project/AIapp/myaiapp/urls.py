from django.urls import path
from .views import SignupView, StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    path('', StudentListView.as_view(), name='student-list'),
    path('student/new/', StudentCreateView.as_view(), name='student-create'),
    path('student/<int:pk>/edit/', StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
]