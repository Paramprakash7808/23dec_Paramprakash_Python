"""
Courses App – Serializers
Handles validation and serialization for Course model.
"""

from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    Used in both Course views and nested inside StudentDetailSerializer.
    """

    # Read-only count of students enrolled in this course
    enrolled_student_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'instructor',
            'duration_weeks',
            'is_active',
            'enrolled_student_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'enrolled_student_count', 'created_at', 'updated_at']

    def get_enrolled_student_count(self, obj):
        """Return the number of students currently enrolled in this course."""
        return obj.enrolled_students.count()
