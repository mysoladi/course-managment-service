from rest_framework import serializers
from . import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['course_name', 'course_description']

    def create(self, validated_data):
        return models.Course.objects.create(**validated_data)
    
class assignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assignment
        fields = ['title', 'assignment_description', 'due_date']

    def create(self, validated_data):
        return models.Assignment.objects.create(**validated_data)
