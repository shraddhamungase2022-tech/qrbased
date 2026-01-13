from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'department', 'year', 'created_at')
    search_fields = ('name', 'roll_number')
    list_filter = ('department', 'year')
    readonly_fields = ('student_id', 'created_at', 'updated_at')
