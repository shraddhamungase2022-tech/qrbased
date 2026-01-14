from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('student/<uuid:student_id>/', views.student_id, name='student_id'),
    path('verify/', views.verify_student, name='verify_student'),
    path('api/verify/', views.verify_api, name='verify_api'),
    path('download-qr/<uuid:student_id>/', views.download_qr, name='download_qr'),
    path('delete-student/<uuid:student_id>/', views.delete_student, name='delete_student'),
    path('edit-student/<uuid:student_id>/', views.edit_student, name='edit_student'),
]
