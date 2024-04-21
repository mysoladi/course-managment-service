from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_fileupload'),  # Ensure the dependency is on the last migration that applied successfully
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='grade',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
