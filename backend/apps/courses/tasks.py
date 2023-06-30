from celery import shared_task
from datetime import date
from django.db.models import Q
from courses.models import Course, CourseStatus


@shared_task
def change_course_status_to_in_progress():
    '''
    filter all courses with status of ENROLLING
    with start date of today and change status to IN_PROGRESS
    '''
    today = date.today()
    courses = Course.objects.filter(
        status=CourseStatus.ENROLLING,
        start_date__lte=today,
        end_date__gt=today
    )
    courses.update(status=CourseStatus.IN_PROGRESS)
    return f'Changed status to IN_PROGRESS for {courses.count()} courses'


@shared_task
def change_course_status_to_completed():
    '''
    filter all courses with status of IN_PROGRESS
    with end date of today and change status to COMPLETED
    '''
    today = date.today()
    courses = Course.objects.filter(
        ~Q(status=CourseStatus.COMPLETED),
        Q(end_date__lte=today)
    )
    courses.update(status=CourseStatus.COMPLETED)
    return f'Changed status to COMPLETED for {courses.count()} courses'
