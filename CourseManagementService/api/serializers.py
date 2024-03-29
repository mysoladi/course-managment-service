from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'course_description']

    def create(self, validated_data):
        return Course.objects.create(**validated_data)
