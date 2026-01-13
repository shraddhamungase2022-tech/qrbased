#!/usr/bin/env python
"""
Script to populate database with sample data for testing
Run: python manage.py shell < populate_data.py
"""

from qr_app.models import Student
from django.core.files.base import ContentFile
import qrcode
import io
import json

# Sample data
students_data = [
    {
        'name': 'Rajesh Kumar',
        'roll_number': 'CSE001',
        'department': 'CSE',
        'year': '3',
    },
    {
        'name': 'Priya Singh',
        'roll_number': 'ECE002',
        'department': 'ECE',
        'year': '2',
    },
    {
        'name': 'Amit Patel',
        'roll_number': 'ME003',
        'department': 'ME',
        'year': '1',
    },
    {
        'name': 'Anjali Verma',
        'roll_number': 'CE004',
        'department': 'CE',
        'year': '4',
    },
    {
        'name': 'Vikram Singh',
        'roll_number': 'EE005',
        'department': 'EE',
        'year': '3',
    },
]

def create_qr_code(student):
    """Generate QR code for student"""
    qr_data = {
        'student_id': str(student.student_id),
        'name': student.name,
        'roll_number': student.roll_number,
        'department': student.department,
        'year': student.year
    }
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer

# Clear existing students
print("Clearing existing students...")
Student.objects.all().delete()

# Create sample students
print("Creating sample students...")
for data in students_data:
    student = Student.objects.create(**data)
    
    # Generate and save QR code
    qr_buffer = create_qr_code(student)
    qr_filename = f'qr_{student.roll_number}.png'
    student.qr_code.save(qr_filename, ContentFile(qr_buffer.getvalue()), save=True)
    
    print(f"✓ Created: {student.name} ({student.roll_number})")

print(f"\nSuccessfully created {len(students_data)} students with QR codes!")
print("\nYou can now:")
print("1. Login as admin at /admin-login/")
print("2. View students in admin dashboard at /admin-dashboard/")
print("3. Verify students at /verify/")
