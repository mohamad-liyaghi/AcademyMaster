# Enrollments Application Documentation

The Enrollments application is responsible for managing enrollments and their related data within the Academy Master project. This document provides a comprehensive overview of the application's models, views, permissions, signals, Celery Beat tasks, and tests.
Once a course is created, students can enroll in it. 

## Table of Contents

- [Models](#models)
  - [Enrollment](#enrollment)
  - [EnrollmentStatus](#enrollmentstatus)
- [Views](#views)
  - [EnrollmentCreateView](#enrollmentcreateview)
  - [EnrollmentRetrieveView](#enrollmentretrieveview)
  - [EnrollmentUpdateView](#enrollmentupdateview)
  - [EnrollmentListView](#enrollmentlistview)
- [Permissions](#permissions)
  - [CanRetrieveEnrollment](#canretrieveenrollment)
- [Signals](#signals)
  - [send_enrollment_email](#send_enrollment_email)
- [Celery Beat Tasks](#celery-beat-tasks)
  - [auto_delete_pending_enrollment](#auto_delete_pending_enrollment)
- [Tests](#tests)

## Models

### Enrollment

The `Enrollment` model represents an enrollment within the Academy Master project. It contains fields such as course, user, status, created_at, and price.

### EnrollmentStatus

`EnrollmentStatus` is a TextChoices field that represents the status of an enrollment. It includes choices such as PENDING, SUCCESS, and FAILED.

## Views

### EnrollmentCreateView

`EnrollmentCreateView` is responsible for creating new enrollments. Only students can create enrollments. It accepts a POST request with the necessary data and returns responses based on the request's validity and the user's authorization.

### EnrollmentRetrieveView

`EnrollmentRetrieveView` is responsible for retrieving an enrollment's details. The enrollment can be retrieved by the enrolled user or a manager. It accepts a GET request and returns responses based on the request's validity and the user's authorization.

### EnrollmentUpdateView

`EnrollmentUpdateView` is responsible for updating an enrollment's status to success or failed. It accepts a PUT/PATCH request with the updated data and returns responses based on the request's validity and the user's authorization.

### EnrollmentListView

`EnrollmentListView` is responsible for listing all enrollments. If the user is a manager, all enrollments are listed. It returns responses based on the user's login status and authorization.

## Permissions

### CanRetrieveEnrollment

`CanRetrieveEnrollment` permission allows only managers and the object owner to retrieve an enrollment.

## Signals

### send_enrollment_email

The `send_enrollment_email` signal is responsible for sending an email when an enrollment is created.

## Celery Beat Tasks

### auto_delete_pending_enrollment

The `auto_delete_pending_enrollment` task deletes pending enrollments after a day without payment.

## Tests

The tests for the Enrollments application are located in the `enrollments/tests` folder. They can be run using the following command:

```
pytest apps/enrollments/
```

These tests ensure that all functionalities of the Enrollments application are working as expected.