@echo off
REM Student QR System - Windows Setup Script

echo ===================================
echo Student QR Verification System
echo Setup for Windows
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo [STEP 1] Creating Virtual Environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

echo [STEP 2] Activating Virtual Environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

echo [STEP 3] Installing Dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo [STEP 4] Running Migrations...
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Failed to run migrations
    pause
    exit /b 1
)
echo [OK] Database migrations completed
echo.

echo [STEP 5] Creating Admin User...
echo.
echo Enter admin credentials:
echo Username: admin
echo Email: admin@example.com
echo Password: admin123
echo.
python manage.py shell << EOF
from django.contrib.auth.models import User
try:
    User.objects.get(username='admin')
    print("[INFO] Admin user already exists")
except User.DoesNotExist:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("[OK] Admin user created: admin / admin123")
EOF
echo.

echo [STEP 6] Collecting Static Files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo [WARNING] Failed to collect static files (non-critical)
)
echo.

echo ===================================
echo Setup Complete!
echo ===================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then open: http://localhost:8000/
echo.
echo Admin Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Admin Dashboard: http://localhost:8000/admin-login/
echo Django Admin: http://localhost:8000/admin/
echo.
pause
