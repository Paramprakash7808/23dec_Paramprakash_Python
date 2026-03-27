"""
Courses App – URL Configuration

All course-related endpoints:
    GET/POST             /api/courses/
    GET/PUT/PATCH/DELETE /api/courses/<id>/
    GET                  /api/courses/<id>/students/
"""

from django.urls import path
from .views import CourseListCreateView, CourseDetailView, CourseStudentsView

urlpatterns = [
    # List all courses / Create new course
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),

    # Get / Update / Delete a single course
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Get all students enrolled in a course
    path('courses/<int:pk>/students/', CourseStudentsView.as_view(), name='course-students'),
]
