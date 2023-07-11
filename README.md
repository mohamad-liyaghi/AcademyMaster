# AcademyMaster

## Introduction <a name="introduction"></a>
AcademyMaster is a user-friendly, open-source web application designed to streamline academic institution management. With a focus on simplifying managing courses, teachers, student activities, and enrollments.<br> The platform offers varying access levels for administrators, managers, teachers, and students to meet each user group's specific needs.

## Backend <a name="backend"></a>
The backend of AcademyMaster is built using Django and Django REST Framework, incorporating modern technologies such as Docker, PostgreSQL, Redis, Celery, RabbitMQ, and Elastic Search. This solid technology stack ensures efficient data management and a smooth user experience.
For detailed information about the AcademyMaster backend, please refer to the [Backend Docs](backend/README.md).

## Frontend <a name="frontend"></a>
The front-end of AcademyMaster is currently undergoing maintenance. We welcome contributions from front-end developers to help enhance and further develop the user experience.

## How to Run <a name="how-to-run"></a>
Follow these simple steps to run the AcademyMaster backend:

1. Clone the project repository:
    ```bash
    git clone https://github.com/mohamad-liyaghi/AcademyMaster.git
    ```

2. Change to the project directory:
    ```bash
    cd AcademyMaster/
    ```

3. To run the project in development mode using Docker-compose, execute the following command:
    ```bash
    docker-compose up --build
    ```

   If you want to run the project in production mode, use the following command instead:
    ```bash
    docker-compose -f docker-compose.prod.yml up --build
    ```

   This will build and start the containers required for the project to run in a production environment.

4. Access the AcademyMaster API in a web browser at `http://localhost:8000/`.

You're all set! Enjoy using AcademyMaster to manage your academic institution with ease.
