from rest_framework import serializers
from .models import Student, Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    # To correctly display course details along with student details when reading,
    # but still accept primary keys for writing, we can map `courses` field.
    courses_details = CourseSerializer(source='courses', many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'courses', 'courses_details']
        extra_kwargs = {
            'courses': {'write_only': True}
        }
