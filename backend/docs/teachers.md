# Teachers Application Documentation

The Teachers application is a crucial component of the Academy Master project, responsible for managing teacher-related data and operations. This document provides a comprehensive overview of the application's models, views, permissions, signals, and tests.

## Table of Contents

- [Models](#models)
  - [Teacher](#teacher)
- [Views](#views)
  - [TeacherCreateView](#teachercreateview)
  - [TeacherUpdateView](#teacherupdateview)
  - [TeacherDeleteView](#teacherdeleteview)
  - [TeacherRetrieveView](#teacherretrieveview)
  - [TeacherListView](#teacherlistview)
- [Permissions](#permissions)
  - [CanAddTeacher](#canaddteacher)
  - [CanDeleteTeacher](#candeleteteacher)
  - [CanUpdateTeacher](#canupdateteacher)
- [Signals](#signals)
  - [SendTeacherPromotionEmail](#sendteacherpromotionemail)
- [Tests](#tests)

## Models

### Teacher

The `Teacher` model is the primary model in the Teachers application. It inherits from `AbstractToken` and `AbstractPermission` and represents a teacher within the Academy Master project.
The `Teacher` model has the following fields:
- `user`: A foreign key relationship to the associated `Account` model.
- `promoted_by`: A foreign key relationship to the `Account` model of the user who promoted the teacher.
- `promotion_date`: A datetime field representing the date the teacher was promoted.
- `description`: A text field containing a brief description of the teacher's role.
- `contact_links`: A JSON field containing the teacher's contact links (e.g., Twitter, LinkedIn, GitHub).

## Views

### TeacherCreateView

`TeacherCreateView` is responsible for creating new teachers. It accepts a POST request with the user's email and returns various responses based on the request's validity and the user's authorization.

### TeacherUpdateView

`TeacherUpdateView` is used for updating an existing teacher's information. It accepts a PUT/PATCH request with the user's updated description and contact_links.

### TeacherDeleteView

`TeacherDeleteView` is used for deleting a teacher. It accepts a DELETE request and returns responses based on the request's validity and the user's authorization.

### TeacherRetrieveView

`TeacherRetrieveView` is used for retrieving a teacher's details. It accepts a GET request and returns responses based on the request's validity and the user's authorization.

### TeacherListView

`TeacherListView` is used for listing all teachers and their associated information. It returns responses based on the user's login status.

## Permissions

### CanAddTeacher

`CanAddTeacher` permission ensures that the user is a manager and has the `teachers.add_teacher` permission.

### CanDeleteTeacher

`CanDeleteTeacher` permission ensures that the user is a manager and has the `teachers.delete_teacher` permission.

### CanUpdateTeacher

`CanUpdateTeacher` permission ensures that the user is the object owner.

## Signals

### SendTeacherPromotionEmail

The `send_teacher_promotion_email` signal is triggered when a new teacher is created. It sends an email to the new teacher notifying them of their promotion.

## Tests

The tests for the Teachers application are located in the `apps/teachers` directory. They can be run using the following command:

```
pytest apps/teachers/
```
This ensures that all functionalities of the Teachers application are working as expected.