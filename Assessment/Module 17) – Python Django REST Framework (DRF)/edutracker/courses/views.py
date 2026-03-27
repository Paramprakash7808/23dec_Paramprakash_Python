"""
Courses App – Views
RESTful API views for Course CRUD operations.

Endpoints:
    GET     /api/courses/         → List all courses
    POST    /api/courses/         → Add a new course
    GET     /api/courses/<id>/    → Get single course (with enrolled students)
    PUT     /api/courses/<id>/    → Update course details (full update)
    PATCH   /api/courses/<id>/    → Partial update course details
    DELETE  /api/courses/<id>/    → Delete a course
    GET     /api/courses/<id>/students/  → List all students enrolled in a course
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Course
from .serializers import CourseSerializer


class CourseListCreateView(APIView):
    """
    GET  /api/courses/  → Return list of all courses
    POST /api/courses/  → Create a new course (requires auth)
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Return all courses."""
        courses = Course.objects.prefetch_related('enrolled_students').all()
        serializer = CourseSerializer(courses, many=True)
        return Response({
            'count': courses.count(),
            'results': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new course."""
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """
    GET    /api/courses/<id>/  → Retrieve single course
    PUT    /api/courses/<id>/  → Full update
    PATCH  /api/courses/<id>/  → Partial update
    DELETE /api/courses/<id>/  → Delete course
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        """Return a single course."""
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Fully update a course."""
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partially update a course."""
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a course."""
        course = self.get_object(pk)
        course.delete()
        return Response(
            {'message': 'Course deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class CourseStudentsView(APIView):
    """
    GET /api/courses/<id>/students/
    Returns all students currently enrolled in a specific course.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        from students.serializers import StudentSerializer
        students = course.enrolled_students.all()
        serializer = StudentSerializer(students, many=True)
        return Response({
            'course': course.title,
            'enrolled_count': students.count(),
            'students': serializer.data,
        }, status=status.HTTP_200_OK)
