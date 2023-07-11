# AcademyMaster Backend

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies](#technologies)
3. [Applications](#applications)
    - [Core](#core)
    - [Accounts](#accounts)
    - [Profiles](#profiles)
    - [Managers](#managers)
    - [Teachers](#teachers)
    - [Courses](#courses)
    - [Enrollments](#enrollments)
    - [Activities](#activities)
4. [Recap](#recap)
5. [How to Run](#how-to-run)

## Introduction <a name="introduction"></a>
AcademyMaster is a web application designed to efficiently manage all aspects of an academic institution. Built with Django and Django REST Framework, this platform provides comprehensive features for course management, student activities, enrollments, and managing teachers. <br>

AcademyMaster supports 4 user roles: `admin`, `manager`, `teacher`, and `student`.<br>
The admin, is basically a superuser, it has full access to all platform features. <br>
Managers have permission to manage courses and teachers (Based on their permissions). Teachers are responsible for being assigned to courses, while students can enroll in courses and access their class activities which teachers updated them.<br>
<br>
This documentation provides an in-depth overview of the AcademyMaster backend, including the technologies used, the various applications within the project, and instructions on how to run the backend locally.<br>

## Technologies <a name="technologies"></a>
The AcademyMaster platform utilizes the following technologies:
1. Django
2. Django REST Framework
3. Docker
4. PostgreSQL
5. Redis
6. Celery
7. RabbitMQ
8. Swagger
9. JWT
10. Elastic Search

## Applications <a name="applications"></a>
The project is structured into seven main applications and a core module.

### Core <a name="core"></a>
The `core` module is a fundamental part of the project and houses common functions and classes that are utilized throughout the platform. It includes models such as `AbstractToken` for generating unique tokens and `AbstractPermission` for handling permission-related tasks. The module also provides celery tasks for sending emails and pytest fixtures for testing API endpoints. Additionally, it includes serializers for representing various relations and views for handling error responses. For more detailed information, please refer to the [Full Document](docs/core.md).

### Accounts <a name="accounts"></a>
The `Accounts` application is responsible for managing user accounts and their verification process. It includes models such as `Account` for storing user information and `VerificationCode` for generating and managing verification codes. The application provides views for user registration, email verification, resending verification codes, and generating JWT tokens for authentication. It also includes signals for generating verification codes and sending verification emails. Additionally, there are Celery Beat tasks for deleting expired verification codes and deactivated users. The application offers custom manager methods for verifying codes and utility functions for generating unique verification codes. It also defines exceptions for handling various scenarios related to user accounts and verification. For more detailed information, please refer to the [Full Document](docs/accounts.md).

### Profiles <a name="profiles"></a>
The `Profiles` application is responsible for managing user profiles within the Academy Master project. It includes the `Profile` model, which stores additional information about users such as their profile picture, date of birth, passport ID, and phone number. The application provides views for retrieving and updating user profiles, with appropriate permissions to ensure only the profile owner or users with specific roles can access and modify the profiles. The application also includes a signal that automatically creates a profile for an active user when their account is activated. Additionally, the application provides tests to ensure the functionality of the profile-related features. For more detailed information, please refer to the [Full Document](docs/profiles.md).

### Managers <a name="managers"></a>
The `Managers` application is responsible for managing managers and their permissions within the Academy Master project. It provides models, views, and utilities to handle the promotion, demotion, and management of managers. The application includes the `Manager` model, which represents a manager and contains fields for the associated user, the user who promoted them, and the promotion date. The application also provides a custom model manager, `ManagerManager`, for adding and updating permissions for managers. Signals are used to send email notifications when a new manager is promoted. The application includes views for creating, updating, retrieving, and deleting managers, with appropriate permissions to ensure only authorized users can perform these actions. Additionally, the application defines permissions to control access to manager-related functionality. The application also provides tests to ensure the functionality of the manager-related features. For more detailed information, please refer to the [Full Document](docs/managers.md).

### Teachers <a name="teachers"></a>
The `Teachers` application is responsible for managing teacher-related data and operations within the Academy Master project. It provides models, views, permissions, signals, and tests to handle the promotion and management of teachers. The application includes the `Teacher` model, which represents a teacher and contains fields for the associated user, the user who promoted them, the promotion date, a description of their role, and contact links. The application provides views for creating, updating, retrieving, and deleting teachers, with appropriate permissions to ensure only authorized users can perform these actions. Signals are used to send email notifications when a new teacher is promoted. The application also defines permissions to control access to teacher-related functionality. Additionally, the application includes tests to ensure the functionality of the teacher-related features. For more detailed information, please refer to the [Full Document](docs/teachers.md).

### Courses <a name="courses"></a>
The `Courses` application is responsible for managing courses and their associated data within the Academy Master project. It provides models, views, permissions, documents, Celery Beat tasks, and tests to handle the creation, management, and status changes of courses. The application includes the `Course` model, which represents a course and contains fields for storing information such as title, description, location, instructor, start date, end date, schedule, days, session count, prerequisite, level, status, and price. The application also includes models for representing the course level and status as choices. Views are provided for creating, retrieving, updating, and deleting courses, with appropriate permissions to ensure only authorized users can perform these actions. The application also includes a document for searching courses using Elasticsearch and Celery Beat tasks for automatically changing the status of courses. Additionally, the application provides tests to ensure the functionality of the course-related features. For more detailed information, please refer to the [Full Document](docs/courses.md).

### Enrollments <a name="enrollments"></a>
The `Enrollments` application is responsible for managing enrollments and their related data within the Academy Master project. It provides models, views, permissions, signals, Celery Beat tasks, and tests to handle the creation, retrieval, update, and listing of enrollments. The application includes the `Enrollment` model, which represents an enrollment and contains fields for storing information such as the course, user, status, created date, and price. The application also includes a model for representing the enrollment status as choices. Views are provided for creating, retrieving, updating, and listing enrollments, with appropriate permissions to ensure only authorized users can perform these actions. Signals are used to send email notifications when an enrollment is created. Celery Beat tasks are used to automatically delete pending enrollments after a specified period. Additionally, the application provides tests to ensure the functionality of the enrollment-related features. For more detailed information, please refer to the [Full Document](docs/enrollments.md).

### Activities <a name="activities"></a>
The `Activities` application manages student activities within the Academy Master project, handling attendance records, final marks, and more. It includes models, methods, signals, views, and permissions to provide a comprehensive solution for managing term activities. Refer to the [Full Document](docs/activities.md) for a detailed overview.

## Recap <a name="recap"></a>
The Core module contains common functions and classes used throughout the project. It includes models like `AbstractToken` and `AbstractPermission`, Celery tasks, serializers, and error views. <br>

The Accounts application handles user accounts and verification. It includes models like `Account` and `VerificationCode`, views for registration and authentication, signals, and Celery Beat tasks.<br>

The Profiles application manages user profiles. It includes the `Profile` model and views to retrieve and update profiles. A signal creates profiles when accounts are activated.<br>

The Managers application handles manager promotions and permissions. It includes the `Manager` model, a ManagerManager model manager, signals, views, and permissions.<br>

The Teachers application handles teacher promotions and data. It includes the `Teacher` model, views, signals, and permissions. <br>

The Courses application handles course creation, management, and status changes. It includes the `Course` model, views, permissions, documents, Celery Beat tasks, and models for course level and status.<br>

The `Enrollments` application handles enrollments and related data. It includes the Enrollment model, views, permissions, signals, Celery Beat tasks, and a model for enrollment status.<br>

In summary, admins can promote users to managers, who can promote teachers and assign courses. Students can enroll in courses and view activities which are updated by teachers.

## How to Run <a name="how-to-run"></a>
To run the backend of this project, ensure Docker and Docker-compose are installed on your machine. Follow these steps:

1. Clone the project:
    ```bash
    git clone https://github.com/mohamad-liyaghi/AcademyMaster.git
    ```

2. Navigate to the project's backend folder:
    ```bash
    cd AcademyMaster/backend
    ```

3. Run it using Docker-compose:
    ```bash
    docker-compose up --build
    ```

4. Open a browser and navigate to `http://localhost:8000/`.


To run tests, execute the following command:

```bash
docker exec  -it academy-master-backend pytest
```

Enjoy using AcademyMaster!