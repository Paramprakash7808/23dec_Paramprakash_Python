"""
Students App – Serializers
Handles validation and serialization for Student model.
"""

from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    """
    Full serializer for Student model.
    Includes enrolled_courses as a list of course primary keys.
    Supports create and update with course linking via ManyToMany.
    """

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'enrolled_courses',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports at module load time
        from courses.models import Course
        self.fields['enrolled_courses'] = serializers.PrimaryKeyRelatedField(
            many=True,
            read_only=False,
            queryset=Course.objects.all(),
            required=False,
        )

    def create(self, validated_data):
        """Create a student and set ManyToMany courses if provided."""
        courses = validated_data.pop('enrolled_courses', [])
        student = Student.objects.create(**validated_data)
        student.enrolled_courses.set(courses)
        return student

    def update(self, instance, validated_data):
        """Update student fields and optionally update enrolled courses."""
        courses = validated_data.pop('enrolled_courses', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if courses is not None:
            instance.enrolled_courses.set(courses)

        return instance


class StudentDetailSerializer(serializers.ModelSerializer):
    """
    Read-only nested serializer — returns full course objects inside a student.
    Used in GET single student for richer response.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Import here to avoid circular imports at module load time
        from courses.serializers import CourseSerializer
        self.fields['enrolled_courses'] = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'enrolled_courses',
            'created_at',
            'updated_at',
        ]
