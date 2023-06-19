from django.contrib import admin
from teachers.models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'promotion_date']
