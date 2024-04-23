from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_course_course_description_course_course_name_and_more"),
    ]

    operations = [
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
                ("grade", models.IntegerField(blank=True, null=True)),  # Changed from CharField to IntegerField
            ],
        ),
    ]
