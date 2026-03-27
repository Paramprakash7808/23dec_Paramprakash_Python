"""
Courses App – Tests
Tests all CRUD operations for Course API using DRF's APIClient.
Covers: list, create, retrieve, update (PUT/PATCH), delete, student listing.
Run with: python manage.py test courses
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from courses.models import Course
from students.models import Student


class CourseAPITestCase(TestCase):
    """Base setup shared across all course test cases."""

    def setUp(self):
        self.client = APIClient()

        # Authenticated user + token
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Sample courses
        self.course1 = Course.objects.create(
            title='Python Basics',
            description='Learn Python from scratch.',
            instructor='Alice Smith',
            duration_weeks=8,
            is_active=True,
        )
        self.course2 = Course.objects.create(
            title='Web Development',
            description='HTML, CSS, JS.',
            instructor='Charlie Brown',
            duration_weeks=10,
            is_active=False,
        )

        # Student enrolled in course1
        self.student = Student.objects.create(
            first_name='Test',
            last_name='Student',
            email='student@example.com',
        )
        self.student.enrolled_courses.set([self.course1])


class TestCourseList(CourseAPITestCase):
    """GET /api/courses/ – List all courses."""

    def test_get_all_courses_returns_200(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_courses_count(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.data['count'], 2)

    def test_list_unauthenticated_allowed(self):
        self.client.credentials()
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCourseCreate(CourseAPITestCase):
    """POST /api/courses/ – Add a new course."""

    def test_create_course_returns_201(self):
        data = {
            'title': 'Machine Learning',
            'description': 'Intro to ML algorithms.',
            'instructor': 'Dr. Data',
            'duration_weeks': 12,
        }
        response = self.client.post('/api/courses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Machine Learning')

    def test_create_course_missing_title_returns_400(self):
        data = {'instructor': 'No Title'}
        response = self.client.post('/api/courses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_course_unauthenticated_returns_401(self):
        self.client.credentials()
        data = {'title': 'Unauthorized', 'instructor': 'Hacker', 'duration_weeks': 1}
        response = self.client.post('/api/courses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCourseRetrieve(CourseAPITestCase):
    """GET /api/courses/<id>/ – Retrieve a single course."""

    def test_get_single_course_returns_200(self):
        response = self.client.get(f'/api/courses/{self.course1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python Basics')

    def test_get_course_includes_enrolled_count(self):
        response = self.client.get(f'/api/courses/{self.course1.id}/')
        self.assertIn('enrolled_student_count', response.data)
        self.assertEqual(response.data['enrolled_student_count'], 1)

    def test_get_nonexistent_course_returns_404(self):
        response = self.client.get('/api/courses/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCourseUpdate(CourseAPITestCase):
    """PUT/PATCH /api/courses/<id>/ – Update course."""

    def test_put_update_course_returns_200(self):
        data = {
            'title': 'Python Advanced',
            'instructor': 'Alice Smith',
            'duration_weeks': 10,
            'is_active': True,
        }
        response = self.client.put(
            f'/api/courses/{self.course1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Python Advanced')

    def test_patch_update_course_instructor(self):
        data = {'instructor': 'New Instructor'}
        response = self.client.patch(
            f'/api/courses/{self.course1.id}/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['instructor'], 'New Instructor')

    def test_update_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.patch(
            f'/api/courses/{self.course1.id}/', {'title': 'Hacked'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCourseDelete(CourseAPITestCase):
    """DELETE /api/courses/<id>/ – Delete a course."""

    def test_delete_course_returns_204(self):
        response = self.client.delete(f'/api/courses/{self.course2.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted_course_no_longer_exists(self):
        self.client.delete(f'/api/courses/{self.course2.id}/')
        self.assertFalse(Course.objects.filter(pk=self.course2.id).exists())

    def test_delete_nonexistent_course_returns_404(self):
        response = self.client.delete('/api/courses/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.delete(f'/api/courses/{self.course1.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCourseStudentsList(CourseAPITestCase):
    """GET /api/courses/<id>/students/ – List all students in a course."""

    def test_get_course_students_returns_200(self):
        response = self.client.get(f'/api/courses/{self.course1.id}/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_students_correct_count(self):
        response = self.client.get(f'/api/courses/{self.course1.id}/students/')
        self.assertEqual(response.data['enrolled_count'], 1)
        self.assertEqual(response.data['students'][0]['email'], 'student@example.com')

    def test_get_students_nonexistent_course_returns_404(self):
        response = self.client.get('/api/courses/9999/students/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
