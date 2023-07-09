# Core Module Documentation

This documentation provides a comprehensive overview of the Core Module, which houses common functions and classes utilized throughout the project. 

## Table of Contents
1. [Models](#models)
    - AbstractPermission
    - AbstractToken
    - WeekDays
2. [Celery Tasks](#celery-tasks)
    - Send Email
3. [Pytest Fixtures](#pytest-fixtures)
    - Client
    - Unique UUID
4. [Permissions](#permissions)
    - IsManager
    - IsTeacher
    - IsStudent
    - IsNonStudent
    - IsObjectOwner
5. [Serializer](#serializer)
    - PermissionSerializer
    - UserRelationSerializer
    - ProfileRelationSerializer
    - UserProfileRelationSerializer
    - InstructorRelationSerializer
    - CourseRelationSerializer
    - EnrollmentRelationSerializer
6. [Views](#views)
    - handler_404
    - handler_500

## Models <a name="models"></a>

### AbstractPermission
The `AbstractPermission` handles the permission related tasks. This model provides some methods that can be used while inheriting from it.
methods:
- `get_subclass_permissions()`: A class method which returns all permissons of the subclass.
- `get_permission(action: str)`: A class method which returns the permission of a class, based on the action.
- `_get_permission_for_model(app_labels: list, model_names: list)`: A class method which returns the permissions based on app_labels and model_names.


### AbstractToken
The AbstractToken class is an abstract model with a `token` field. All models inheriting from this class will generate a unique token upon object creation.

### WeekDays
The WeekDays model is a choice field containing all days of the week.

## Celery Tasks <a name="celery-tasks"></a>

### Send Email
The `send_email` task is a background process responsible for sending emails throughout the project. It requires `subject`, `to_email`, `context`, and `template_name` as arguments.

## Pytest Fixtures <a name="pytest-fixtures"></a>

### Client
The `api_client` fixture provides an `APIClient` client for testing API endpoints.

### Unique UUID
The `unique_uuid` fixture provides a unique uuid for testing based on the time.

## Permissions <a name="permissions"></a>

### IsManager
This permission checks if the user is a manager.

### IsTeacher
This permission checks if the user is a teacher.

### IsStudent
This permission checks if the user is a student.

### IsNonStudent
This permission verifies that the user is not a student, but a manager, teacher, or admin.

### IsObjectOwner
This permission checks if the user is the owner of the object.

## Serializer <a name="serializer"></a>

### PermissionSerializer
This base serializer represents permissions via codename.

### UserRelationSerializer
This base serializer represents user relations by first_name, last_name, and email.

### ProfileRelationSerializer
This base serializer represents profile relations by user, avatar, birth_date, and profile token.

### UserProfileRelationSerializer
This serializer combines UserRelationSerializer and ProfileRelationSerializer to represent a user with its profile data.

### InstructorRelationSerializer
This base serializer previews course instructor.

### CourseRelationSerializer
This base serializer previews courses in activities or enrollments.

### EnrollmentRelationSerializer
This base serializer previews enrollments in activities.

## Views <a name="views"></a>

### handler_404
This view handles 404 errors, returning a JSON response with a 404 status code.

### handler_500
This view handles 500 errors, returning a JSON response with a 500 status code and logging the error.