# Accounts Application Documentation

Table of Contents:
- [Models](#models)
  - [Account](#account)
  - [AccountRole](#accountrole)
  - [VerificationCode](#verificationcode)
- [Views](#views)
  - [Register](#register)
  - [Verify](#verify)
  - [ResendCode](#resendcode)
  - [JWT Token](#jwt-token)
- [Signals](#signals)
  - [Create Verification Token](#create-verification-token)
  - [Send Code by Email](#send-code-by-email)
- [Celery Beat Tasks](#celery-beat-tasks)
  - [Delete Expired Codes](#delete-expired-codes)
  - [Delete Deactivated Users](#delete-deactivated-users)
- [Custom Manager Methods](#custom-manager-methods)
  - [Verify](#verify)
- [Utils](#utils)
  - [Generate Unique Verification Code](#generate-unique-verification-code)
- [Model Exceptions](#model-exceptions)
  - [DuplicationCodeException](#duplicationcodeexception)
  - [ActiveUserCodeException](#activeusercodeexception)
- [Serializer Exceptions](#serializer-exceptions)
  - [UserAlreadyExistsException](#useralreadyexistsexception)
  - [PendingVerificationException](#pendingverificationexception)
  - [AlreadyVerifiedException](#alreadyverifiedexception)
  - [DuplicationCodeException](#duplicationcodeexception-1)
- [Tests](#tests)

## Models

### Account

The `Account` model represents a user account and saves basic information of each user. It contains the following fields:

- `email`: A unique email address for the user.
- `password`: A hashed password for the user.
- `is_active`: A boolean flag indicating if the user's account is active.
- `first_name`: A string field that saves the user's first name.
- `last_name`: An optional string field that saves the user's last name.
- `date_joined`: A datetime field representing the date the user joined.

### AccountRole

The `AccountRole` is an abstract model which is responsible for checking user roles. It provides the following methods:

- `is_admin()`: Return True if user is superuser.
- `is_manager()`: Return True if user is admin or has a Manager object associated.
- `is_teacher()`: Return True if user is admin or has a Teacher object associated.
- `is_student()`: Return True if user is not admin, manager or teacher.

### VerificationCode

The `VerificationCode` model represents a unique code associated with a user account for the purpose of email verification. Each verification code is valid for only 5 minutes. It contains the following fields:

- `code`: An INT field which saves a 5 digit code.
- `account`: A foreign key relationship to the associated `Account` model.
- `expire_at`: A datetime field representing the expiration date of the verification code.
- `retry_count`: An integer field that saves the number of retries for a verification code.
- `is_expired()`: A method that checks if the verification code has expired.

## Views

### Register

The `UserRegisterView` is responsible for handling user registration. It accepts a POST request containing the user's email and basic information.

- **Request**:
  - Method: POST
  - Data: Email, first name, last name, password

- **Response**:
  - `201 Created`: User registered successfully and pending for verification.
  - `202 Accepted`: A user with the same email exists and is pending verification.
  - `400 Bad Request`: An active user already exists with the provided email.

### Verify

The `UserVerifyView` is responsible for handling email verification. It accepts a POST request containing a verification code. If the code is valid and not expired, the associated user account's `is_active` field is set to `True`.

- **Request**:
  - Method: POST
  - Data: Verification code

- **Response**:
  - `200 OK`: User verified.
  - `400 Bad Request`: Invalid verification code.
  - `409 Conflict`: User is already verified.

### ResendCode

The `ResendCodeView` handles resending verification codes. It accepts a POST request containing a user's email. If an active verification code already exists, it returns a 200 OK response. Otherwise, it generates a new verification code and sends it to the user's email.

- **Request**:
  - Method: POST
  - Data: User's email

- **Response**:
  - `201 Created`: New verification code generated and sent.
  - `200 Accepted`: An active verification code already exists.
  - `400 Bad Request`: Invalid data.

### JWT Token

The `TokenObtainView` handles authentication and generates JWT tokens. It accepts a POST request containing a user's email and password. If the credentials are valid and the user's email has been verified, a JWT token is generated and returned in the response.

- **Request**:
  - Method: POST
  - Data: User's email and password

- **Response**:
  - `200 OK`: Token generated successfully.
  - `400 Bad Request`: Invalid credentials.

## Signals

### Create Verification Token

The `generate_verification_code()` signal is triggered when a new user account is created. It generates a unique verification code and associates it with the user account. Each code is only active for 5 minutes.

### Send Code by Email

The `send_verification_email()` signal is triggered when a new verification token is created. It sends an email to the user containing a link to verify their account, including the unique verification code.

## Celery Beat Tasks

### Delete Expired Codes

The `delete_expired_codes()` task runs periodically and is responsible for deleting expired verification codes from the database.

### Delete Deactivated Users

The `delete_deactivated_users()` task runs periodically and is responsible for removing deactivated users who haven't verified their accounts within the last 24 hours.

## Custom Manager Methods

### Verify

The `verify` method from `VerificationCodeManager` class is responsible for checking a verification code. It checks the status of expirations and other details.

## Utils

### Generate Unique Verification Code

The `generate_unique_verification_code()` utility function generates a unique 5-digit verification code for a user.

## Model Exceptions

### DuplicationCodeException

Raised when trying to create a valid code twice.

### ActiveUserCodeException

Raised when attempting to create a verification code for an active user.

## Serializer Exceptions

### UserAlreadyExistsException

This exception is raised when an attempt is made to create a new user account with an email that already has an active user associated with it. Status is 400.

### PendingVerificationException

This exception is raised when an attempt is made to create a new user account with an email that already has a pending verification. Status is 200.

### AlreadyVerifiedException

This exception is raised when an attempt is made to verify an email address that is already verified. Status is 409.

### DuplicationCodeException

This exception is raised when attempting to resend a verification code while an active code already exists. Status is 409.

## Tests

The tests for the Accounts application can be found in the `apps/accounts` directory.

Run them with the following command:

```
pytest apps/accounts
```