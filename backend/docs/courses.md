# Courses Application Documentation

The Courses application is a crucial component of the Academy Master project, responsible for managing courses and their associated data. This document provides a comprehensive overview of the application's models, views, permissions, documents, Celery Beat tasks, and tests.

## Table of Contents

- [Models](#models)
  - [Course](#course)
  - [CourseLevel](#courselevel)
  - [CourseStatus](#coursestatus)
- [Views](#views)
  - [CourseCreateView](#coursecreateview)
  - [CourseRetrieveView](#courseretrieveview)
  - [CourseUpdateView](#courseupdateview)
  - [CourseDeleteView](#coursedeleteview)
  - [CourseListView](#courselistview)
- [Permissions](#permissions)
  - [CanAddCourse](#canaddcourse)
  - [CanUpdateCourse](#canupdatecourse)
  - [CanDeleteCourse](#candeletecourse)
- [Documents](#documents)
  - [CourseDocument](#coursedocument)
- [Celery Beat Tasks](#celery-beat-tasks)
  - [change_course_status_to_in_progress](#change_course_status_to_in_progress)
  - [change_course_status_to_completed](#change_course_status_to_completed)
- [Tests](#tests)

## Models

### Course

The `Course` model represents a course within the Academy Master project. It contains various fields to store information about the course, such as title, description, location, instructor, start date, end date, schedule, days, session count, prerequisite, level, status, and price.

### CourseLevel

`CourseLevel` is a TextChoices field that represents the different levels of a course. It includes choices such as A1 (Beginner), A2 (Elementary), B1 (Pre-Intermediate), B2 (Intermediate), C1 (Upper-Intermediate), and C2 (Advanced).

### CourseStatus

`CourseStatus` is a TextChoices field that represents the status of a course. It includes choices such as ENROLLING, IN_PROGRESS, and COMPLETED.

## Views

### CourseCreateView

`CourseCreateView` is responsible for creating new courses and assigning them to a teacher. It accepts a POST request with the necessary data and returns the following responses:

- '201': 'Created' - The course was successfully created.
- '400': 'Bad Request' - The request data is invalid.
- '401': 'Unauthorized' - The user is not authorized to create a course.
- '403': 'Forbidden' - The user does not have permission to create a course.

### CourseRetrieveView

`CourseRetrieveView` is responsible for retrieving a course's details. It accepts a GET request and returns the following responses:

- '200': 'OK' - The course details were successfully retrieved.
- '401': 'Unauthorized' - The user is not authorized to access the course.
- '404': 'Not Found' - The requested course does not exist.

### CourseUpdateView

`CourseUpdateView` is responsible for updating an existing course's information. It accepts a PUT/PATCH request with the updated data and returns the following responses:

- '200': 'OK' - The course was successfully updated.
- '400': 'Bad Request' - The request data is invalid or the course is not in the ENROLLING status.
- '401': 'Unauthorized' - The user is not authorized to update the course.
- '403': 'Forbidden' - The user does not have permission to update the course.
- '404': 'Not Found' - The requested course does not exist.

### CourseDeleteView

`CourseDeleteView` is responsible for deleting a course. It accepts a DELETE request and returns the following responses:

- '204': 'No Content' - The course was successfully deleted.
- '400': 'Bad Request' - The course cannot be deleted if it is in progress or completed.
- '403': 'Forbidden' - The user does not have permission to delete the course.
- '404': 'Not Found' - The requested course does not exist.

### CourseListView

`CourseListView` is responsible for listing all courses and their associated information. It also accepts a search query parameter (`search`) to search for courses using Elasticsearch. It returns the following responses:

- '200': 'OK' - The list of courses was successfully retrieved.
- '401': 'Unauthorized' - The user is not authorized to access the course list.

## Permissions

### CanAddCourse

`CanAddCourse` permission allows only managers with the `courses.add_course` permission to add new courses.

### CanUpdateCourse

`CanUpdateCourse` permission allows only managers with the `courses.change_course` permission to update unfinished courses.

### CanDeleteCourse

`CanDeleteCourse` permission allows only managers with the `courses.delete_course` permission to delete unfinished courses.

## Documents

### CourseDocument

`CourseDocument` is an Elasticsearch document responsible for searching courses by their title and description.

## Celery Beat Tasks

### change_course_status_to_in_progress

`change_course_status_to_in_progress` task filters all courses with a status of `ENROLLING` and a start date of today. It changes their status to `IN_PROGRESS`.

### change_course_status_to_completed

`change_course_status_to_completed` task filters all courses with a status of `IN_PROGRESS` and an end date of today. It changes their status to `COMPLETED`.

## Tests

The tests for the Courses application are located in the `apps/courses` directory. They can be run using the following command:

```
pytest apps/courses/
```

These tests ensure that all functionalities of the Courses application are working as expected.