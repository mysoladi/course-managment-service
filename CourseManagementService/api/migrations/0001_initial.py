# Generated by Django 4.2.11 on 2024-04-23 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Channels",
            fields=[
                ("room_id", models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("course_id", models.AutoField(primary_key=True, serialize=False)),
                ("course_name", models.TextField(default="None", max_length=50)),
                (
                    "course_description",
                    models.TextField(default="None", max_length=400),
                ),
                ("people", models.JSONField(default=list)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            (
                                "Pending",
                                "Pending course that has not been approved by system admin",
                            ),
                            ("Approved", "Approved course that has not yet began"),
                            ("Denied", "Denied course"),
                            ("Active", "Ongoing course"),
                            ("Concluded", "Course that has concluded"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("joinable", models.BooleanField(default=False)),
                ("visible", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="FileUpload",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("file", models.FileField(upload_to="uploads/")),
                ("grade", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("message_id", models.AutoField(primary_key=True, serialize=False)),
                ("sender_id", models.IntegerField()),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="messages",
                        to="api.channels",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="channels",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rooms",
                to="api.course",
            ),
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                ("assignment_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("author", models.IntegerField()),
                ("due_date", models.DateField()),
                ("is_published", models.BooleanField(default=False)),
                ("description", models.TextField()),
                ("file", models.TextField(default="path/to/default/file.ext")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignments",
                        to="api.course",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "announcement_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=255)),
                ("author", models.IntegerField()),
                ("message", models.TextField()),
                ("date", models.DateField(auto_now_add=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="announcements",
                        to="api.course",
                    ),
                ),
            ],
        ),
    ]
