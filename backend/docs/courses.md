# Courses Application Documentation

The Courses application is responsible for managing courses and their related data within the Academy Master project. It provides the necessary models, views, and utilities to manage courses, course levels, and course statuses.

## Table of Contents

1. [Models](#models)
    - [Course](#course)
    - [CourseLevel](#courselevel)
    - [CourseStatus](#coursestatus)
2. [Views](#views)
    - [CourseCreateView](#coursecreateview)
    - [CourseRetrieveView](#courseretrieveview)
    - [CourseUpdateView](#courseupdateview)
    - [CourseDeleteView](#coursedeleteview)
    - [CourseListView](#courselistview)
3. [Permissions](#permissions)
    - [CanAddCourse](#canaddcourse)
    - [CanUpdateCourse](#canupdatecourse)
    - [CanDeleteCourse](#candeletecourse)
4. [Documents](#documents)
    - [CourseDocument](#coursedocument)
5. [Celery Beat Tasks](#celerybeattasks)
    - [change_course_status_to_in_progress](#changecoursestatustoinprogress)
    - [change_course_status_to_completed](#changecoursestatustocompleted)

## Models

### Course

The `Course` model represents a course within the Academy Master project and contains the following fields:

- `title`: A char field containing the course title.
- `description`: A text field containing the course description.
- `location`: A char field containing the course location.
- `instructor`: A foreign key relationship to the associated `Teacher` model.
- `assigned_by`: A foreign key relationship to the `Account` model of the user who assigned the course.
- `start_date`: A date field representing the course start date.
- `end_date`: A date field representing the course end date.
- `schedule`: A JSON field containing the course schedule.
- `days`: An ArrayField of `core.WeekDays` choices representing the course days.
- `session_count`: An integer field representing the number of sessions in the course.
- `prerequisite`: A foreign key relation containing the course prerequisite object id.
- `level`: A field using the `CourseLevel` TextChoices.
- `status`: A field using the `CourseStatus` TextChoices.
- `price`: An INT field representing the course price.

### CourseLevel

`CourseLevel` is a TextChoices field with the following choices:

- A1 - Beginner
- A2 - Elementary
- B1 - Pre-Intermediate
- B2 - Intermediate
- C1 - Upper-Intermediate
- C2 - Advance

### CourseStatus

`CourseStatus` is a TextChoices field with the following choices:

- ENROLLING
- IN_PROGRESS
- COMPLETED

## Views

### CourseCreateView

This view is responsible for creating new courses and assigning them to a teacher. The expected responses are:

- '201': 'ok'
- '400': 'Invalid data'
- '401': 'Unauthorized'
- '403': 'Permission denied'

### CourseRetrieveView

This view is responsible for retrieving a course's details. The expected responses are:

- '200': 'ok'
- '401': 'Unauthorized'
- '404': 'Not found'

### CourseUpdateView

This view is responsible for updating an existing course's information. The expected responses are:

- '200': 'ok'
- '400': 'Course is not enrolling'
- '403': 'Permission denied'
- '404': 'Not found'

### CourseDeleteView

This view is responsible for deleting a course. The expected responses are:

- '204': 'ok'
- '400': 'Cannot delete in-progress/completed courses.'
- '403': 'Permission denied'
- '404': 'Not found'

### CourseListView

This view is responsible for listing all courses and their associated information. It also accepts a search query parameter (`search`) to search courses via Elasticsearch. The expected responses are:

- '200': 'ok'
- '401': 'Unauthorized'

## Permissions

### CanAddCourse

This permission allows only admins and managers with the `courses.add_course` permission to add new courses.

### CanUpdateCourse

This permission allows only the course assigner and managers with the `courses.change_course` permission to update unfinished courses.

### CanDeleteCourse

This permission allows only the course assigner and managers with the `courses.delete_course` permission to update unfinished courses.

## Documents

### CourseDocument

This Elasticsearch document is responsible for searching courses by `title` and `description`.

## Celery Beat Tasks

### change_course_status_to_in_progress

This task filters all courses with a status of `ENROLLING` and a start date of today and changes their status to `IN_PROGRESS`.

### change_course_status_to_completed

This task filters all courses with a status of `IN_PROGRESS` and an end date of today and changes theirstatus to `COMPLETED`.


## Tests

The Courses application is well-tested. To run the tests for the Profiles application, use the following command:

```
pytest apps/courses/
```