"""
Students App – Tests
Tests all CRUD operations for Student API using DRF's APIClient.
Covers: list, create, retrieve, update (PUT/PATCH), delete, enroll/unenroll.
Run with: python manage.py test students
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from students.models import Student
from courses.models import Course


class StudentAPITestCase(TestCase):
    """Base setup shared across all student test cases."""

    def setUp(self):
        """
        Set up:
         - An authenticated user with token
         - Two sample courses
         - Two sample students
        """
        self.client = APIClient()

        # Create a user and token for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create sample courses
        self.course1 = Course.objects.create(
            title='Python Basics',
            instructor='Alice Smith',
            duration_weeks=8,
        )
        self.course2 = Course.objects.create(
            title='Django REST Framework',
            instructor='Bob Jones',
            duration_weeks=6,
        )

        # Create sample students
        self.student1 = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
        )
        self.student1.enrolled_courses.set([self.course1])

        self.student2 = Student.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
        )


class TestStudentList(StudentAPITestCase):
    """GET /api/students/ – List all students."""

    def test_get_all_students_returns_200(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_students_returns_correct_count(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.data['count'], 2)

    def test_get_all_students_unauthenticated_allowed(self):
        """Read-only is allowed without auth (IsAuthenticatedOrReadOnly)."""
        self.client.credentials()  # Remove auth
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestStudentCreate(StudentAPITestCase):
    """POST /api/students/ – Create a new student."""

    def test_create_student_returns_201(self):
        data = {
            'first_name': 'Alice',
            'last_name': 'Wonder',
            'email': 'alice@example.com',
        }
        response = self.client.post('/api/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'alice@example.com')

    def test_create_student_with_courses(self):
        data = {
            'first_name': 'Bob',
            'last_name': 'Builder',
            'email': 'bob@example.com',
            'enrolled_courses': [self.course1.id, self.course2.id],
        }
        response = self.client.post('/api/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.course1.id, response.data['enrolled_courses'])
        self.assertIn(self.course2.id, response.data['enrolled_courses'])

    def test_create_student_duplicate_email_returns_400(self):
        data = {
            'first_name': 'John',
            'last_name': 'Duplicate',
            'email': 'john.doe@example.com',  # already exists
        }
        response = self.client.post('/api/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_missing_email_returns_400(self):
        data = {'first_name': 'NoEmail', 'last_name': 'Student'}
        response = self.client.post('/api/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_student_unauthenticated_returns_401(self):
        self.client.credentials()
        data = {
            'first_name': 'Unauth',
            'last_name': 'User',
            'email': 'unauth@example.com',
        }
        response = self.client.post('/api/students/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestStudentRetrieve(StudentAPITestCase):
    """GET /api/students/<id>/ – Get a single student."""

    def test_get_single_student_returns_200(self):
        response = self.client.get(f'/api/students/{self.student1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'john.doe@example.com')

    def test_get_single_student_has_nested_courses(self):
        response = self.client.get(f'/api/students/{self.student1.id}/')
        self.assertIn('enrolled_courses', response.data)
        # Nested courses should be objects (from StudentDetailSerializer)
        courses = response.data['enrolled_courses']
        self.assertIsInstance(courses, list)
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]['title'], 'Python Basics')

    def test_get_nonexistent_student_returns_404(self):
        response = self.client.get('/api/students/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestStudentUpdate(StudentAPITestCase):
    """PUT/PATCH /api/students/<id>/ – Update student details."""

    def test_put_update_student_returns_200(self):
        data = {
            'first_name': 'John',
            'last_name': 'Updated',
            'email': 'john.doe@example.com',
            'enrolled_courses': [],
        }
        response = self.client.put(
            f'/api/students/{self.student1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], 'Updated')

    def test_patch_update_student_phone(self):
        data = {'phone': '9999999999'}
        response = self.client.patch(
            f'/api/students/{self.student1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '9999999999')

    def test_update_unauthenticated_returns_401(self):
        self.client.credentials()
        data = {'first_name': 'Hacker'}
        response = self.client.patch(
            f'/api/students/{self.student1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestStudentDelete(StudentAPITestCase):
    """DELETE /api/students/<id>/ – Delete a student."""

    def test_delete_student_returns_204(self):
        response = self.client.delete(f'/api/students/{self.student1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted_student_no_longer_exists(self):
        self.client.delete(f'/api/students/{self.student1.id}/')
        self.assertFalse(Student.objects.filter(pk=self.student1.id).exists())

    def test_delete_nonexistent_student_returns_404(self):
        response = self.client.delete('/api/students/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.delete(f'/api/students/{self.student1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestStudentEnroll(StudentAPITestCase):
    """POST/DELETE /api/students/<id>/enroll/ – Enroll/unenroll from courses."""

    def test_enroll_student_in_course(self):
        data = {'course_id': self.course2.id}
        response = self.client.post(
            f'/api/students/{self.student2.id}/enroll/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.course2, self.student2.enrolled_courses.all())

    def test_unenroll_student_from_course(self):
        data = {'course_id': self.course1.id}
        response = self.client.delete(
            f'/api/students/{self.student1.id}/enroll/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.course1, self.student1.enrolled_courses.all())

    def test_enroll_missing_course_id_returns_400(self):
        response = self.client.post(
            f'/api/students/{self.student1.id}/enroll/', {}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_enroll_nonexistent_course_returns_404(self):
        data = {'course_id': 9999}
        response = self.client.post(
            f'/api/students/{self.student1.id}/enroll/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
