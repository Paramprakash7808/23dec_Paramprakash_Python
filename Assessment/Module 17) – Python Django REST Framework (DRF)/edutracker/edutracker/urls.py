"""
EduTracker Solutions – Root URL Configuration
Registers all API endpoints for students, courses, and auth.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    EduTracker Solutions – API Root
    Returns a directory of all available endpoints.
    """
    base = request.build_absolute_uri('/').rstrip('/')
    return Response({
        "message": "Welcome to EduTracker Solutions API",
        "version": "1.0",
        "endpoints": {
            "auth": {
                "obtain_token":     f"{base}/api/auth/token/   [POST]",
            },
            "students": {
                "list_create":      f"{base}/api/students/            [GET, POST]",
                "retrieve_update_delete": f"{base}/api/students/<id>/  [GET, PUT, PATCH, DELETE]",
                "enroll_unenroll":  f"{base}/api/students/<id>/enroll/ [POST, DELETE]",
            },
            "courses": {
                "list_create":      f"{base}/api/courses/             [GET, POST]",
                "retrieve_update_delete": f"{base}/api/courses/<id>/  [GET, PUT, PATCH, DELETE]",
                "enrolled_students": f"{base}/api/courses/<id>/students/ [GET]",
            },
            "admin":              f"{base}/admin/",
        }
    })


urlpatterns = [
    # API Root – welcome page with endpoint directory
    path('', api_root, name='api-root'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Token Authentication endpoint
    # POST /api/auth/token/  →  { "username": "...", "password": "..." }
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),

    # Student API routes
    path('api/', include('students.urls')),

    # Course API routes
    path('api/', include('courses.urls')),
]
