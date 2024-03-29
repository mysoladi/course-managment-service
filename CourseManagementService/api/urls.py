from django.urls import path
from . import views

urlpatterns = [
    # Greetings
    # Course management endpoints
    path('add/', views.AddCourse.as_view(), name='add_course'),
]