# Teachers Application Documentation

The Teachers application is responsible for managing teachers and their permissions within the Academy Master project. It provides the necessary models, views, and utilities to manage teachers and their associated permissions.

## Table of Contents

1. [Models](#models)
    - [Teacher](#teacher)
2. [Views](#views)
    - [TeacherCreateView](#teachercreateview)
    - [TeacherUpdateView](#teacherupdateview)
    - [TeacherDeleteView](#teacherdeleteview)
    - [TeacherRetrieveView](#teacherretrieveview)
    - [TeacherListView](#teacherlistview)
3. [Permissions](#permissions)
    - [CanAddTeacher](#canaddteacher)
    - [CanDeleteTeacher](#candeleteteacher)
    - [IsObjectOwner](#isobjectowner)
4. [Signals](#signals)
    - [SendTeacherPromotionEmail](#sendteacherpromotionemail)
5. [Tests](#tests)

## Models

### Teacher

The `Teacher` model represents a teacher within the Academy Master project. It contains the following fields:

- `user`: A foreign key relationship to the associated `Account` model.
- `promoted_by`: A foreign key relationship to the `Account` model of the user who promoted the teacher.
- `promotion_date`: A datetime field representing the date the teacher was promoted.
- `description`: A text field containing a brief description of the teacher's role.
- `social_fields`: A JSON field containing the teacher's social media accounts (e.g., Twitter, LinkedIn, GitHub).

## Views

### TeacherCreateView

This view is responsible for creating new teachers. It accepts a POST request containing the user's email.

### TeacherUpdateView

This view is responsible for updating an existing teacher's information. It accepts a PUT/PATCH request containing the user's updated description, and social fields.

### TeacherDeleteView

This view is responsible for deleting a teacher. It accepts a DELETE request.

### TeacherRetrieveView

This view is responsible for retrieving a teacher's details. It accepts a GET request.

### TeacherListView

This view is responsible for listing all teachers and their associated information.

## Permissions

### CanAddTeacher

This permission allows users with the `teachers.add_teacher` permission to add new teachers.

### CanDeleteTeacher

This permission allows users with the `teachers.delete_teacher` permission to delete teachers.

### IsObjectOwner
This permission allows teachers to update their informations.

## Signals

### SendTeacherPromotionEmail

This signal is triggered when a new teacher is created. It sends an email to the new teacher notifying them of their promotion.

## Tests

This application is well-tested. To run the tests for the Teachers application, use the following command:

```
pytest apps/teachers/
```