from django.db import models

class Course(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending course that has not been approved by system admin'),
        ('Approved', 'Approved course that has not yet began'),
        ('Denied', 'Denied course'),
        ('Active', 'Ongoing course'),
        ('Concluded', 'Course that has concluded'),
    )
    course_id = models.AutoField(primary_key=True)
    course_name = models.TextField(max_length=50, default="None")
    course_description = models.TextField(max_length=400, default="None")
    people = models.JSONField(default=list)  # Store user IDs as a list of integers
    instructors = models.JSONField(default=list)  # Store instructor user IDs as a list of integers
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    joinable = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)

class Channels(models.Model):
    room_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='rooms')

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Channels, on_delete=models.CASCADE, related_name='messages')

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.IntegerField()
    due_date = models.DateField()
    is_published = models.BooleanField(default=False)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')

class Announcement(models.Model):
    announcement_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.IntegerField()
    message = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='announcements')
