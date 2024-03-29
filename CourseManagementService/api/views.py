from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import CourseSerializer

class AddCourse(APIView):
    def post(self, request):
        # Create a new course instance using the serializer

        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            # Save the course instance
            course = serializer.save()
            course.save()
        
            # Additional logic for handling 'people' list if needed
            # For example, adding users to the course
            return JsonResponse({"message": "Course added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
