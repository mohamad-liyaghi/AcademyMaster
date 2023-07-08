# Activities Application Documentation

The Activities application is responsible for managing student activities during a term, such as attendance records and final marks, within the Academy Master project. This document provides a comprehensive overview of the application's models, model methods, signals, views, permissions, and tests.

## Table of Contents

- [Models](#models)
  - [Activity](#activity)
- [Model Methods](#model-methods)
  - [__validate_enrollment](#__validate_enrollment)
  - [__validate_final_mark](#__validate_final_mark)
- [Signals](#signals)
  - [create_activity_after_successful_enrollment](#create_activity_after_successful_enrollment)
  - [send_email_after_activity_creation](#send_email_after_activity_creation)
- [Views](#views)
  - [ActivityRetrieveView](#activityretrieveview)
  - [ActivityUpdateView](#activityupdateview)
  - [CourseActivityListView](#courseactivitylistview)
- [Permissions](#permissions)
  - [CanRetrieveActivity](#canretrieveactivity)
  - [CanUpdateActivity](#canupdateactivity)
  - [IsCourseInstructor](#iscourseinstructor)
- [Tests](#tests)

## Models

### Activity

The `Activity` model represents a user's activity within a term in the Academy Master project. It contains fields such as course, user, enrollment, attendance, final_mark, and created_at.

## Model Methods

### __validate_enrollment

The `__validate_enrollment` method checks if the user's enrollment is successful. If not, it raises a PermissionDenied.

### __validate_final_mark

The `__validate_final_mark` method checks if the course status is "COMPLETED" before setting the final mark. If the course is not completed, it raises a PermissionDenied.

## Signals

### create_activity_after_successful_enrollment

The `create_activity_after_successful_enrollment` signal is responsible for creating an `Activity` instance after a successful enrollment.

### send_email_after_activity_creation

The `send_email_after_activity_creation` signal is responsible for sending an email when an activity is created.

## Views

### ActivityRetrieveView

`ActivityRetrieveView` is responsible for retrieving an activity's details. The activity can be retrieved by non-students and the activity's owner. It accepts a GET request and returns responses based on the request's validity and the user's authorization.

### ActivityUpdateView

`ActivityUpdateView` is responsible for updating an activity. Only the course instructor can update the activity. It accepts a PUT/PATCH request with the updated data and returns responses based on the request's validity and the user's authorization.

### CourseActivityListView

`CourseActivityListView` is responsible for listing all activities of a course. Only the course instructor can retrieve activities of a course. It accepts a GET request and returns responses based on the request's validity and the user's authorization.

## Permissions

### CanRetrieveActivity

`CanRetrieveActivity` permission allows non-students and the activity's owner to retrieve the activity.

### CanUpdateActivity

`CanUpdateActivity` permission allows only the course instructor to update the activity.

### IsCourseInstructor

`IsCourseInstructor` permission allows only the course instructor to retrieve activities of a course.

## Tests

The tests for the Activities application are located in the `activities/tests` directory. They can be run using the following command:

```
pytest apps/activities/
```

These tests ensure that all functionalities of the Activities application are working as expected.