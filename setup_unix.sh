#!/bin/bash

# Student QR System - macOS/Linux Setup Script

echo "==================================="
echo "Student QR Verification System"
echo "Setup for macOS/Linux"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

echo "[OK] Python found"
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

echo "[STEP 1] Creating Virtual Environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to create virtual environment"
    exit 1
fi
echo "[OK] Virtual environment created"
echo ""

echo "[STEP 2] Activating Virtual Environment..."
source venv/bin/activate
echo "[OK] Virtual environment activated"
echo ""

echo "[STEP 3] Installing Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "[OK] Dependencies installed"
echo ""

echo "[STEP 4] Running Migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to run migrations"
    exit 1
fi
echo "[OK] Database migrations completed"
echo ""

echo "[STEP 5] Creating Admin User..."
echo ""
echo "Admin Credentials:"
echo "  Username: admin"
echo "  Email: admin@example.com"
echo "  Password: admin123"
echo ""

python manage.py shell << 'EOF'
from django.contrib.auth.models import User
try:
    User.objects.get(username='admin')
    print("[INFO] Admin user already exists")
except User.DoesNotExist:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("[OK] Admin user created: admin / admin123")
EOF
echo ""

echo "[STEP 6] Collecting Static Files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "[WARNING] Failed to collect static files (non-critical)"
fi
echo ""

echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then open: http://localhost:8000/"
echo ""
echo "Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Admin Dashboard: http://localhost:8000/admin-login/"
echo "Django Admin: http://localhost:8000/admin/"
echo ""
