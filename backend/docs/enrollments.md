# Enrollments Application Documentation

The Enrollments application is responsible for managing enrollments and their related data within the Academy Master project. It provides the necessary models, views, and utilities to manage enrollments and enrollment statuses.

## Table of Contents

1. [Models](#models)
    - [Enrollment](#enrollment)
    - [EnrollmentStatus](#enrollmentstatus)
2. [Views](#views)
    - [EnrollmentCreateView](#enrollmentcreateview)
    - [EnrollmentRetrieveView](#enrollmentretrieveview)
    - [EnrollmentUpdateView](#enrollmentupdateview)
    - [EnrollmentListView](#enrollmentlistview)
3. [Permissions](#permissions)
    - [AllowStudentOnly](#allowstudentonly)
    - [IsManagerOrStudent](#ismanagerorstudent)
    - [IsObjectOwner](#isobjectowner)
4. [Signals](#signals)
    - [send_enrollment_email](#sendenrollmentemail)
5. [Celery Beat Tasks](#celerybeattasks)
    - [auto_delete_pending_enrollment](#autodeletependingenrollment)

## Models

### Enrollment

The `Enrollment` model represents an enrollment within the Academy Master project and contains the following fields:

- `course`: A foreign key relationship to the associated `Course` model.
- `user`: A foreign key relationship to the `Account` model of the user who enrolled in the course.
- `status`: A field using the `EnrollmentStatus` TextChoices.
- `created_at`: A datetime field representing the enrollment creation date.
- `price`: An INT field representing the enrollment price.

### EnrollmentStatus

`EnrollmentStatus` is a TextChoices field with the following choices:

- PENDING
- SUCCESS
- FAILED

## Views

### EnrollmentCreateView

This is responsible for creating new enrollments. Only students can create enrollments. The expected responses are:

- '201': 'ok'
- '400': 'Bad request'
- '401': 'Unauthorized'
- '403': 'Permission denied'

### EnrollmentRetrieveView

This view is responsible for retrieving an enrollment's details. The enrollment can be retrieved by the enrolled user or a manager. The expected responses are:

- '200': 'ok'
- '401': 'Unauthorized'
- '403': 'Permission denied'
- '404': 'Not found'

### EnrollmentUpdateView

This view is responsible for updating an enrollment's status to success or failed. The expected responses are:

- '200': 'ok'
- '400': 'Bad request'
- '401': 'Unauthorized'
- '403': 'Permission denied'
- '404': 'Not found'

### EnrollmentListView

This view is responsible for listing all enrollments. If the user is a manager, all enrollments are listed. The expected responses are:

- '200': 'ok'
- '401': 'Unauthorized'
- '403': 'Permission denied'

## Permissions

### AllowStudentOnly

This permission allows only students to access the view.

### IsManagerOrStudent

This permission allows only managers and students to access the page.

### IsObjectOwner

This permission allows only managers and the object owner to access the object.

## Signals

### send_enrollment_email

This signal is responsible for sending an email when an enrollment is created.

## Celery Beat Tasks

### auto_delete_pending_enrollment

This task deletes pending enrollments after a day without payment.

## Tests

The Enrollments application is well-tested. To run the tests for the Enrollments application, use the following command:

```
pytest apps/enrollments/
```