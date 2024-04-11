from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import serializers
from . import models

class AddCourse(APIView):
    def post(self, request):
        # Create a new course instance using the serializer

        serializer = serializers.CourseSerializer(data=request.data)
        if serializer.is_valid():
            # Grab the Instructor's ID (The person submitting the course)
            user_id = self.request.query_params.get('user_id')
            user_role = self.request.query_params.get('user_role')
            if user_role not in ['Instructor', 'Admin']:
                return Response({"message": "User is not instructor or admin."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Modify the people data to be a list of dictionaries
            people_data = [{"user_id": user_id, "title": "Instructor"}]
            serializer.validated_data['people'] = people_data

            # Save the course
            serializer.save()
        
            return JsonResponse({"message": "Course added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RemoveCourse(APIView):
    def put(self, request):
        # Grab the Admin's ID (The person removing the course)
        user_id = self.request.query_params.get('user_id')
        user_role = self.request.query_params.get('user_role')
        if user_role != 'Admin':
            return Response({"message": "User is not an Admin."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')

        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Delete the course
        course.delete()

        return JsonResponse({"message": "Course removed successfully"}, status=status.HTTP_201_CREATED)
    
class ApproveCourse(APIView):
    def put(self, request):
        # Grab the Admin's ID (The person removing the course)
        user_id = self.request.query_params.get('user_id')
        user_role = self.request.query_params.get('user_role')
        if user_role != 'Admin':
            return Response({"message": "User is not an Admin."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')

        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Update the course status to "Approved" and set joinable and visible to True
        course.status = 'Approved'
        course.joinable = True
        course.visible = True

        # Save the updated course
        course.save()

        return Response({"message": "Course approved successfully"}, status=status.HTTP_200_OK)
    
class DenyCourse(APIView):
    def put(self, request):
        # Grab the Admin's ID (The person removing the course)
        user_id = self.request.query_params.get('user_id')
        user_role = self.request.query_params.get('user_role')
        if user_role != 'Admin':
            return Response({"message": "User is not an Admin."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')

        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Update the course status to "Denied"
        course.status = 'Denied'
        course.joinable = False
        course.visible = False

        # Save the updated course
        course.save()

        return Response({"message": "Course denied successfully"}, status=status.HTTP_200_OK)
    
class ActivateCourse(APIView):
    def put(self, request):
        # Grab the Instructor's ID (The person activating the course)
        user_id = self.request.query_params.get('user_id')

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')
        
        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Iterate over the people dictionary in the course
        for person in course.people:
            id = person.get('user_id')
            title = person.get('title')

            if id == user_id and title == 'Instructor':
                # Update the course status to "Active"
                course.status = 'Active'
                course.visible = True
                course.joinable = False

                # Save the updated course
                course.save()

                return Response({"message": "Course activated successfully"}, status=status.HTTP_200_OK)

        # If the loop completes without finding a matching instructor, return an error response
        return Response({"message": "Failed to activate course. User is not the instructor."}, status=status.HTTP_400_BAD_REQUEST)
            
class ConcludeCourse(APIView):
    def put(self, request):
        # Grab the Instructor's ID (The person concluding the course)
        user_id = self.request.query_params.get('user_id')

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')

        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Iterate over the people dictionary in the course
        for person in course.people:
            id = person.get('user_id')
            title = person.get('title')

            if id == user_id and title == 'Instructor':
                # Update the course status to "Concluded"
                course.status = 'Concluded'
                course.visible = False
                course.joinable = False

                # Save the updated course
                course.save()
                return Response({"message": "Course concluded successfully"}, status=status.HTTP_200_OK)
        # If the loop completes without finding a matching instructor, return an error response
        return Response({"message": "Failed to activate course. User is not the instructor."}, status=status.HTTP_400_BAD_REQUEST)
    
class GetCourseList(APIView):
    def get(self, request):
        # Retrieve user_id from query parameters
        user_id = request.query_params.get('user_id')

        # Query all courses from the database where the people list contains the user_id
        courses = models.Course.objects.filter(people__contains=[{'user_id': user_id}],status='Approved')

        # Serialize the course instances into JSON format
        serializer = serializers.CourseSerializer(courses, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PendingCourseList(APIView):

    def get(self, request):
        # Retrieve user_role from query parameters
        user_role = self.request.query_params.get('user_role')
        if user_role == 'Admin':

            # Query all courses from the database where the people list contains the user_id
            courses = models.Course.objects.filter(status='Pending')
            # Serialize the course instances into JSON format
            serializer = serializers.AdminCourseSerializer(courses, many=True)
            # Return the serialized data as a response
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If the user is not an admin, return an error response
        return Response({"message": "User is not an Admin."}, status=status.HTTP_400_BAD_REQUEST)
    
class ApproveCourseList(APIView):

    def get(self, request):
        # Retrieve user_role from query parameters
        user_role = self.request.query_params.get('user_role')
        if user_role == 'Admin':

            # Query all courses from the database where the people list contains the user_id
            courses = models.Course.objects.filter(status='Approved')
            # Serialize the course instances into JSON format
            serializer = serializers.AdminCourseSerializer(courses, many=True)
            # Return the serialized data as a response
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If the user is not an admin, return an error response
        return Response({"message": "User is not an Admin."}, status=status.HTTP_400_BAD_REQUEST)
    
class DenyCourseList(APIView):

    def get(self, request):
        # Retrieve user_role from query parameters
        user_role = self.request.query_params.get('user_role')
        if user_role == 'Admin':

            # Query all courses from the database where the people list contains the user_id
            courses = models.Course.objects.filter(status='Denied')
            # Serialize the course instances into JSON format
            serializer = serializers.AdminCourseSerializer(courses, many=True)
            # Return the serialized data as a response
            return Response(serializer.data, status=status.HTTP_200_OK)
        # If the user is not an admin, return an error response
        return Response({"message": "User is not an Admin."}, status=status.HTTP_400_BAD_REQUEST)
        
class LeaveCourse(APIView):
    def put(self, request):
        # Retrieve user_id from query parameters
        user_id = request.query_params.get('user_id')
        
        # Retrieve course_id from request data
        course_id = request.data.get('course_id')
        
        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)
        
        # Remove user_id from the course's people list
        course.people = [person for person in course.people if person.get('user_id') != user_id]
        
        # Save the updated course
        course.save()
        
        return Response({"message": f"User {user_id} left course {course_id} successfully"}, status=status.HTTP_200_OK)

class JoinCourse(APIView):
    def put(self, request):
        # Retrieve user_id from query parameters
        user_id = request.query_params.get('user_id')
        
        # Retrieve course_id from request data
        course_id = request.data.get('course_id')
        
        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)
        
        # Add user_id to the course's people list
        course.people.append({"user_id": user_id, "title": "Student"})
        
        # Save the updated course
        course.save()
        
        return Response({"message": f"User {user_id} joined course {course_id} successfully"}, status=status.HTTP_200_OK)

class AddAnnouncement(APIView):
    def post(self, request):
        # Retrieve user_id from query parameters
        user_id = request.query_params.get('user_id')
        
        # Retrieve course_id from request data
        course_id = request.data.get('course_id')

        serializer = serializers.AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            # Save the announcement instance
            serializer.validated_data['author'] = user_id
            serializer.validated_data['course'] = get_object_or_404(models.Course, pk=course_id)
            announcement = serializer.save()
            announcement.save()
            return JsonResponse({"message": "Announcement added successfully"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class RemoveAnnouncement(APIView):
    def put(self, request):
        announcement_id = request.data.get('announcement_id')
        announcement = get_object_or_404(models.Announcement, pk=announcement_id)
        announcement.delete()
        return Response({"message": "Announcement removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class GetAnnouncementList(APIView):
    def get(self, request):
        # Retrieve user_id from query parameters
        user_id = request.query_params.get('user_id')

        course_id = request.query_params.get('course_id')

        # Query all Announcements from the database where the course id matches
        announcements = models.Announcement.objects.filter(course=get_object_or_404(models.Course, pk=course_id))

        # Serialize the announcement instances into JSON format
        serializer = serializers.AnnouncementSerializer(announcements, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddAssignment(APIView):
    def post(self, request):
        # Grab the Instructor's ID (The person activating the course)
        user_id = self.request.query_params.get('user_id')

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')
        
        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Iterate over the people dictionary in the course
        for person in course.people:
            id = person.get('user_id')
            title = person.get('title')

            if id == user_id and title == 'Instructor':
                serializer = serializers.AssignmentSerializer(data=request.data)
                if serializer.is_valid():
                    # Save the assignment instance
                    serializer.validated_data['author'] = user_id
                    serializer.validated_data['course'] = get_object_or_404(models.Course, pk=course_id)
                    announcement = serializer.save()
                    announcement.save()
                    return JsonResponse({"message": "Assignment added successfully"}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # If the loop completes without finding a matching instructor, return an error response
        return Response({"message": "Failed to add assignment. User is not the instructor."}, status=status.HTTP_400_BAD_REQUEST)
    

class RemoveAssignment(APIView):
    def put(self, request):
        # Grab the Instructor's ID (The person removing the assignment)
        user_id = self.request.query_params.get('user_id')

        # Retrieve course_id from request data
        course_id = request.data.get('course_id')
        
        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Iterate over the people dictionary in the course
        for person in course.people:
            id = person.get('user_id')
            title = person.get('title')

            if id == user_id and title == 'Instructor':
                assignment_id = request.data.get('assignment_id')
                assignment = get_object_or_404(models.Assignment, pk=assignment_id)
                assignment.delete()
                return Response({"message": "assignment removed successfully"}, status=status.HTTP_204_NO_CONTENT)
        # If the loop completes without finding a matching instructor, return an error response
        return Response({"message": "Failed to remove assignment. User is not the instructor."}, status=status.HTTP_400_BAD_REQUEST)
    
class GetAssignmentList(APIView):
    def get(self, request):
        # Retrieve user_id from query parameters
        user_id = request.query_params.get('user_id')

        course_id = request.data.get('course_id')

        # Query all Anssignment from the database where the course id matches
        announcements = models.Assignment.objects.filter(course=get_object_or_404(models.Course, pk=course_id))

        # Serialize the course instances into JSON format
        serializer = serializers.AssignmentSerializer(announcements, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PublishAssignment(APIView):
    def put(self, request):
        # Grab the Instructor's ID (The person publishing the assignment)
        user_id = self.request.query_params.get('user_id')

        # Retrieve course_id from request data
        assignment_id = request.data.get('assignment_id')
        # Retrieve assignment_id from request data
        course_id = request.data.get('course_id')

        # Get the assignment instance from the database or return 404 if not found
        assignment = get_object_or_404(models.Assignment, pk=assignment_id)
        # Get the course instance from the database or return 404 if not found
        course = get_object_or_404(models.Course, pk=course_id)

        # Iterate over the people dictionary in the course
        for person in course.people:
            id = person.get('user_id')
            title = person.get('title')

            if id == user_id and title == 'Instructor':
                # Update the assignment is_published status to "True"
                assignment.is_published = True
                # Save the updated course
                assignment.save()
                return Response({"message": "assignment published successfully"}, status=status.HTTP_200_OK)
        # If the loop completes without finding a matching instructor, return an error response
        return Response({"message": "Failed to publish assignment. User is not the instructor."}, status=status.HTTP_400_BAD_REQUEST)