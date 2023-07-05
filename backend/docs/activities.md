# Activities Application Documentation

The Activities application is responsible for managing student activities during a term, such as attendance records and their final marks within the Academy Master project. It provides the necessary models, views, and utilities to manage activities and activity data.

## Table of Contents

1. [Models](#models)
    - [Activity](#activity)
2. [Model Methods](#modelmethods)
    - [__validate_enrollment](#__validate_enrollment)
    - [__validate_final_mark](#__validate_final_mark)
3. [Signals](#signals)
    - [create_activity_after_successful_enrollment](#create_activity_after_successful_enrollment)
    - [send_email_after_activity_creation](#send_email_after_activity_creation)
4. [Views](#views)
    - [ActivityRetrieveView](#activityretrieveview)
    - [ActivityUpdateView](#activityupdateview)
    - [CourseActivityListView](#courseactivitylistview)
5. [Permissions](#permissions)
    - [CanRetrieveActivity](#canretrieveactivity)
    - [CanUpdateActivity](#canupdateactivity)
    - [IsCourseInstructor](#iscourseinstructor)

## Models

### Activity

The `Activity` model represents a user's activity within a term in the Academy Master project and contains the following fields:

- `course`: A foreign key relationship to the associated `Course` model.
- `user`: A foreign key relationship to the `Account` model of the user participating in the course.
- `enrollment`: A foreign key relationship to the associated `Enrollment` model.
- `attendance`: A JSON field representing the user's attendance records.
- `final_mark`: An INT field representing the user's final mark in the course.
- `created_at`: A datetime field representing the activity creation date.

## Model Methods

### __validate_enrollment

This method checks if the user's enrollment is successful. If not, it raises a PermissionDenied.

### __validate_final_mark

This method checks if the course status is "COMPLETED" before setting the final mark. If the course is not completed, it raises a PermissionDenied.

## Signals

### create_activity_after_successful_enrollment

This signal is responsible for creating an `Activity` instance after a successful enrollment.

### send_email_after_activity_creation

This signal is responsible for sending an email when an activity is created.

## Views

### ActivityRetrieveView

This view is responsible for retrieving an activity's details. The activity can be retrieved by non-students and the activity's owner. The expected responses are:

- '200': 'ok'
- '403': 'Forbidden'
- '401': 'Unauthorized'
- '404': 'Not found'

### ActivityUpdateView

This view is responsible for updating an activity. Only the course instructor can update the activity. The expected responses are:

- '200': 'Updated'
- '403': 'Forbidden'
- '401': 'Unauthorized'
- '404': 'Not found'

### CourseActivityListView

This view is responsible for listing all activities of a course. Only the course instructor can retrieve activities of a course. The expected responses are:

- '200': 'ok'
- '403': 'Forbidden'
- '401': 'Unauthorized'
- '404': 'Not found'

## Permissions

### CanRetrieveActivity

This permission allows non-students and the activity's owner to retrieve the activity.

### CanUpdateActivity

This permission allows only the course instructor to update the activity.

### IsCourseInstructor

This permission allows only the course instructor to retrieve activities of a course.

## Tests

The Activities application is well-tested. To run the tests for the Activities application, use the following command:

```
pytest apps/activities/
```