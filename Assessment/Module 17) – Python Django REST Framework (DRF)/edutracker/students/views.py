"""
Students App – Views
RESTful API views for Student CRUD operations.

Endpoints:
    GET     /api/students/          → List all students
    POST    /api/students/          → Add a new student
    GET     /api/students/<id>/     → Get single student (with nested course details)
    PUT     /api/students/<id>/     → Update student details (full update)
    PATCH   /api/students/<id>/     → Partial update student details
    DELETE  /api/students/<id>/     → Delete a student
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Student
from .serializers import StudentSerializer, StudentDetailSerializer


class StudentListCreateView(APIView):
    """
    Handles listing all students and creating a new student.

    GET  /api/students/  → Returns all students (paginated JSON)
    POST /api/students/  → Creates a new student, returns 201 with student data
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Return a list of all students."""
        students = Student.objects.prefetch_related('enrolled_courses').all()
        serializer = StudentSerializer(students, many=True)
        return Response({
            'count': students.count(),
            'results': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new student. Requires authentication."""
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    """
    Handles retrieving, updating, and deleting a single student.

    GET    /api/students/<id>/  → Get single student with nested course info
    PUT    /api/students/<id>/  → Full update of student
    PATCH  /api/students/<id>/  → Partial update of student
    DELETE /api/students/<id>/  → Delete student (returns 204)
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        """Helper: fetch student or return 404."""
        return get_object_or_404(Student, pk=pk)

    def get(self, request, pk):
        """Return a single student with full nested course details."""
        student = self.get_object(pk)
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """Fully update a student record. Requires authentication."""
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partially update a student record. Requires authentication."""
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a student. Requires authentication. Returns 204 No Content."""
        student = self.get_object(pk)
        student.delete()
        return Response(
            {'message': 'Student deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )


class StudentEnrollView(APIView):
    """
    Manages enrolling or unenrolling a student from a specific course.

    POST   /api/students/<id>/enroll/    → Enroll student in a course
    DELETE /api/students/<id>/enroll/    → Unenroll student from a course

    Request body: { "course_id": <int> }
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Student, pk=pk)

    def post(self, request, pk):
        """Enroll the student in a given course."""
        from courses.models import Course

        student = self.get_object(pk)
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'course_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, pk=course_id)
        student.enrolled_courses.add(course)

        return Response(
            {'message': f"Student '{student}' enrolled in course '{course}'."},
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        """Unenroll the student from a given course."""
        from courses.models import Course

        student = self.get_object(pk)
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {'error': 'course_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, pk=course_id)
        student.enrolled_courses.remove(course)

        return Response(
            {'message': f"Student '{student}' unenrolled from course '{course}'."},
            status=status.HTTP_200_OK
        )
