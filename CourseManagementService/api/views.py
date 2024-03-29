from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers

class AddCourse(APIView):
    def post(self, request):
        # Create a new course instance using the serializer

        serializer = serializers.CourseSerializer(data=request.data)
        if serializer.is_valid():
            # Save the course instance
            course = serializer.save()

            user_id = self.request.query_params.get('user_id')

            course.set(
                instructors = {user_id : "Instructor"}
            )

            course.save()
        
            return JsonResponse({"message": "Course added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddAssignment(APIView):
    def post(self, request):
        # Create a new assignment instance using the serializer

        serializer = serializers.assignmentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the assignment instance
            assignment = serializer.save()
            assignment.save()

            return JsonResponse({"message": "Assignment added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
