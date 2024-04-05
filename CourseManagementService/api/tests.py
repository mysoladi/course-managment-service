from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from . import models

class CourseViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user_id = 1
        self.user_role = 'Instructor'

    def test_add_course(self):
        client = Client()
        url = reverse('add_course')
        url += f'?user_id={self.user_id}&user_role={self.user_role}'
        data = {
            'course_name': 'Test Course',
            'course_description': 'Description of Test Course',
        }
        response = client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Course.objects.count(), 1)

    def test_remove_course(self):
        self.user_role = 'Admin'
        # Create a test course
        course = models.Course.objects.create(course_name='Test Course', course_description='Description of Test Course')

        client = Client()
        url = reverse('remove_course')
        url += f'?user_id={self.user_id}&user_role={self.user_role}'
        data = {'course_id': course.course_id}
        response = client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Course.objects.count(), 0)

    def test_approve_course(self):
        self.user_role = 'Admin'
        # Create a test course
        course = models.Course.objects.create(course_name='Test Course', course_description='Description of Test Course')

        client = Client()
        url = reverse('approve_course')
        url += f'?user_id={self.user_id}&user_role={self.user_role}'
        data = {'course_id': course.course_id}
        response = client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Course.objects.get(course_id=course.course_id).status, 'Approved')
    
    def test_deny_course(self):
        self.user_role = 'Admin'
        # Create a test course
        course = models.Course.objects.create(course_name='Test Course', course_description='Description of Test Course')

        client = Client()
        url = reverse('deny_course')
        url += f'?user_id={self.user_id}&user_role={self.user_role}'
        data = {'course_id': course.course_id}
        response = client.put(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course.refresh_from_db()
        self.assertEqual(course.status, 'Denied')
        self.assertFalse(course.joinable)
        self.assertFalse(course.visible)

class AnnouncementViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user_id = 1
        self.user_role = 'Instructor'

    def test_add_announcement(self):
        # Create a test course
        course = models.Course.objects.create(course_name='Test Course', course_description='Description of Test Course')

        client = Client()
        url = reverse('add_announcement')
        url += f'?user_id={self.user_id}&user_role={self.user_role}'
        data = {
            'title': 'Test announcement',
            'message': 'Test123Test',
            'course_id': course.course_id
        }
        response = client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Announcement.objects.count(), 1)

    def test_remove_announcement(self):
        # Create a test course
        course = models.Course.objects.create(course_name='Test Course', course_description='Description of Test Course')
        # Create a test announcement
        announcement = models.Announcement.objects.create(author= self.user_id, title='Test announcement', message='Test123Test', course=course)

        client = Client()
        url = reverse('remove_announcement')
        url += f'?user_id={self.user_id}&user_role={self.user_role}'
        data = {'announcement_id': announcement.announcement_id}
        response = client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Announcement.objects.count(), 0)

    def test_get_announcement_list(self):
        # Create a test course
        course = models.Course.objects.create(course_name='Test Course', course_description='Description of Test Course')
        # Create a test announcement
        announcement = models.Announcement.objects.create(author= self.user_id, title='Test announcement', message='Test123Test', course=course)
        client = Client()
        url = reverse('get_announcement')
        url += f'?user_id={self.user_id}'
        url += f'&course_id={course.course_id}'
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)