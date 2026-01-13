from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('roll_number', models.CharField(max_length=50, unique=True)),
                ('department', models.CharField(choices=[('CSE', 'Computer Science'), ('ECE', 'Electronics'), ('ME', 'Mechanical'), ('CE', 'Civil'), ('EE', 'Electrical')], max_length=50)),
                ('year', models.CharField(choices=[('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year')], max_length=10)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='student_photos/')),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
