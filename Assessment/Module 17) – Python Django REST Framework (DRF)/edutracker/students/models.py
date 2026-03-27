"""
Students App – Models
Defines the Student model with a ManyToMany relationship to Course.
"""

from django.db import models


class Student(models.Model):
    """
    Represents a student enrolled at EduTracker.

    Fields:
        first_name  – Student's first name
        last_name   – Student's last name
        email       – Unique email (used as identifier)
        phone       – Optional phone number
        date_of_birth – Optional date of birth
        enrolled_courses – ManyToMany link to Course (managed from Student side)
        created_at  – Auto timestamp on creation
        updated_at  – Auto timestamp on update
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # ManyToMany relationship: a student can enroll in multiple courses
    # and a course can have multiple students
    enrolled_courses = models.ManyToManyField(
        'courses.Course',
        blank=True,
        related_name='enrolled_students',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
