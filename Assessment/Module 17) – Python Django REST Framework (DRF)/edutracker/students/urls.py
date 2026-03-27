"""
Students App – URL Configuration

All student-related endpoints:
    GET/POST   /api/students/
    GET/PUT/PATCH/DELETE  /api/students/<id>/
    POST/DELETE  /api/students/<id>/enroll/
"""

from django.urls import path
from .views import StudentListCreateView, StudentDetailView, StudentEnrollView

urlpatterns = [
    # List all students / Create new student
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),

    # Get / Update / Delete a single student
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),

    # Enroll / Unenroll a student from a course
    path('students/<int:pk>/enroll/', StudentEnrollView.as_view(), name='student-enroll'),
]
