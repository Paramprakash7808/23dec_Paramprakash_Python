"""
Courses App – Models
Defines the Course model.
"""

from django.db import models


class Course(models.Model):
    """
    Represents a course offered at EduTracker.

    Fields:
        title       – Course title
        description – Detailed description of the course
        instructor  – Name of the instructor delivering the course
        duration_weeks – Length of the course in weeks
        is_active   – Whether this course is currently active/open for enrollment
        created_at  – Auto timestamp on creation
        updated_at  – Auto timestamp on update

    Reverse relations:
        enrolled_students – All students enrolled via Student.enrolled_courses M2M
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=150)
    duration_weeks = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} (by {self.instructor})"
