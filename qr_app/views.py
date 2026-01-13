from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import qrcode
import io
from PIL import Image
from django.core.files.base import ContentFile
import json
import uuid as uuid_lib
import os

from .models import Student
from .forms import StudentForm

# Home Page
def home(request):
    return render(request, 'index.html')

# Admin Login
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an admin!')
    
    return render(request, 'admin_login.html')

# Admin Logout
def admin_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

# Admin Dashboard
@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    
    students = Student.objects.all()
    return render(request, 'admin_dashboard.html', {'students': students})

# Add Student
@login_required(login_url='admin_login')
def add_student(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            
            # Generate QR Code with URL that points to student details page
            # The QR will encode the student detail page URL
            request_scheme = request.scheme
            request_host = request.get_host()
            qr_url = f"{request_scheme}://{request_host}/student/{student.student_id}/"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save QR Code
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qr_filename = f'qr_{student.roll_number}_{uuid_lib.uuid4().hex[:8]}.png'
            student.qr_code.save(qr_filename, ContentFile(buffer.getvalue()), save=False)
            
            student.save()
            messages.success(request, f'Student {student.name} added successfully with QR code!')
            return redirect('admin_dashboard')
    else:
        form = StudentForm()
    
    return render(request, 'add_student.html', {'form': form})

# View Student Details and QR (Mobile-friendly for QR scanning)
def student_id(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, 'student_info.html', {'student': student})

# Verify Student
def verify_student(request):
    result = None
    student = None
    
    if request.method == 'POST':
        qr_data = request.POST.get('qr_data', '').strip()
        
        if qr_data:
            try:
                data = json.loads(qr_data)
                student_id = data.get('student_id')
                
                try:
                    student = Student.objects.get(student_id=student_id)
                    result = {
                        'status': 'valid',
                        'message': f'✅ Valid Student',
                        'student': {
                            'name': student.name,
                            'roll_number': student.roll_number,
                            'department': student.get_department_display(),
                            'year': f"Year {student.year}",
                        }
                    }
                except Student.DoesNotExist:
                    result = {
                        'status': 'invalid',
                        'message': '❌ Invalid Student - Not found in database'
                    }
            except json.JSONDecodeError:
                result = {
                    'status': 'invalid',
                    'message': '❌ Invalid QR Code Format'
                }
        else:
            result = {
                'status': 'invalid',
                'message': '❌ Please provide QR data'
            }
    
    return render(request, 'verify.html', {'result': result})

# API endpoint for verification (for AJAX)
@require_POST
def verify_api(request):
    qr_data = request.POST.get('qr_data', '').strip()
    
    if not qr_data:
        return JsonResponse({'status': 'error', 'message': 'No QR data provided'})
    
    try:
        data = json.loads(qr_data)
        student_id = data.get('student_id')
        
        try:
            student = Student.objects.get(student_id=student_id)
            return JsonResponse({
                'status': 'valid',
                'message': '✅ Valid Student',
                'student': {
                    'name': student.name,
                    'roll_number': student.roll_number,
                    'department': student.get_department_display(),
                    'year': f"Year {student.year}",
                    'photo': student.photo.url if student.photo else None,
                }
            })
        except Student.DoesNotExist:
            return JsonResponse({
                'status': 'invalid',
                'message': '❌ Invalid Student - Not found in database'
            })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'invalid',
            'message': '❌ Invalid QR Code Format'
        })

# Download QR Code
def download_qr(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if student.qr_code:
        return redirect(student.qr_code.url)
    return redirect('student_id', student_id=student_id)
