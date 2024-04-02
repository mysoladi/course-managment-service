from django.urls import path
from . import views

urlpatterns = [
    # Greetings
    # Course management endpoints
    path('course/', views.GetCourseList.as_view(), name='get_course'),
    path('course/add', views.AddCourse.as_view(), name='add_course'),
    path('course/remove', views.RemoveCourse.as_view(), name='remove_course'),
    path('course/approve', views.ApproveCourse.as_view(), name='approve_course'),
    path('course/activate', views.ActivateCourse.as_view(), name='activate_course'),
    path('course/deny', views.DenyCourse.as_view(), name='deny_course'),
    path('course/activate', views.ActivateCourse.as_view(), name='activate_course'),
    path('course/conclude', views.ConcludeCourse.as_view(), name='conclude_course'),
    path('course/join', views.JoinCourse.as_view(), name='join_course'),
    path('course/leave', views.LeaveCourse.as_view(), name='leave_course'),
]