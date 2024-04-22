from rest_framework import serializers
from . import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['course_id', 'course_name', 'course_description']

    def create(self, validated_data):
        return models.Course.objects.create(**validated_data)
    
class AdminCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['course_id', 'people', 'course_description', 'course_name', ]

    def create(self, validated_data):
        return models.Course.objects.create(**validated_data)
    
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assignment
        fields = ['assignment_id','title', 'description', 'due_date','is_published']

    def create(self, validated_data):
        return models.Assignment.objects.create(**validated_data)
    
class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ['title', 'message','date']
    
    def create(self, validated_data):
        return models.Announcement.objects.create(**validated_data)
