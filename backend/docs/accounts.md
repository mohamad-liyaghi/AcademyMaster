# Accounts Application Documentation

The Accounts application is responsible for user authentication and verification within the Academy Master project. It provides models, views, signals, tasks, manager methods, utils, exceptions, and tests to manage user accounts and their associated verification codes.

## Table of Contents

1. [Models](#models)
    - [Account](#account)
    - [VerificationCode](#verificationcode)
    - [AccountRole](#accountrole)
2. [Views](#views)
    - [Register](#register)
    - [Verify](#verify)
    - [Token](#token)
    - [ResendCode](#resendcode)
3. [Signals](#signals)
    - [Create Verification Token](#create-verification-token)
    - [Send by Email](#send-by-email)
4. [Celery Beat Tasks](#celery-beat-tasks)
    - [Delete Expired Codes](#delete-expired-codes)
    - [Delete Deactivated Users](#delete-deactivated-users)
5. [Custom Manager Methods](#custom-manager-methods)
    - [Verify](#verify)
    - [Re-generate](#re-generate)
6. [Utils](#utils)
    - [Generate Unique Verification Code](#generate-unique-verification-code)
7. [Exceptions](#exceptions)
    - [DuplicateUserException](#duplicateuserexception)
    - [PendingVerificationException](#pendingverificationexception)
    - [AlreadyVerifiedException](#alreadyverifiedexception)
    - [DuplicationVerificationCodeException](#duplicationverificationcodeexception)
8. [Tests](#tests)

## Models

### Account

The `Account` model represents a user account. It contains the following fields:

- `email`: A unique email address for the user.
- `password`: A hashed password for the user.
- `is_active`: A boolean flag indicating if the user's account is active.
- `first_name`: A string field that saves the user's first name.
- `last_name`: An optional string field that saves the user's last name.
- `date_joined`: A datetime field representing the date the user joined.

### VerificationCode

The `VerificationCode` model represents a unique code associated with a user account for the purpose of email verification. It contains the following fields:

- `code`: A unique alphanumeric string representing the verification code.
- `account`: A foreign key relationship to the associated `Account` model.
- `expire_at`: A datetime field representing the expiration date of the verification code.
- `retry_count`: An integer field that saves the number of retries for a verification code.
- `is_expired()`: A method that checks if the verification code has expired.

### AccountRole

The `AccountRole` model is responsible for user roles. It provides the following methods:

- `is_admin()`: Checks if the user has an admin role.
- `is_manager()`: Checks if the user has an managers role.
- `is_teacher()`: Checks if the user has an teacher role.
- `is_student()`: Checks if the user has an student role.

## Views

### Register

The `UserRegisterView` view is responsible for handling user registration. It accepts a POST request containing the user's email and basic informations. Upon successful registration, a verification token is created and sent to the user's email.

- **Method**: `POST`
- **Request Body**:
  - `email` (string): The user's email address.
  - `first_name` (string): The user's first name.
  - `last_name` (string): The user's last name.
  - `password` (string): The user's password.
- **Response**:
  - `202 Accepted`: A user with same email exists and pendin to verify.
  - `201 Created`: User registered successfully.
  - `400 Bad Request`: An active user already exists with the provided email.

### Verify

The `UserVerifyView` view is responsible for handling email verification. It accepts a POST request containing a verification code. If the code is valid and not expired, the associated user account's `is_active` field is set to `True`.

- **Method**: `POST`
- **Request Body**:
  - `user` (string): The users token.
  - `code` (string): The verification code.

- **Response**:
  - `200 OK`: Email verified successfully.
  - `400 Bad Request`: Invalid verification code.
  - `409 Conflict`: User is already verified.

### Token

The `TokenObtainView` view handles authentication and generates tokens. It accepts a POST request containing a user's email and password. If the credentials are valid and the user's email has been verified, a JWT token is generated and returned in the response.

- **Method**: `POST`
- **Request Body**:
  - `email` (string): The user's email address.
  - `password` (string): The user's password.
- **Response**:
  - `200 OK`: Token generated successfully.
  - `400 Bad Request`: Invalid credentials.

### ResendCode

The `ResendCodeView` view handles resending verification codes. It accepts a POST request containing a user's email. If an active verification code already exists, it returns a 200 OK response. Otherwise, it generates a new verification code and sends it to the user's email.

- **URL**: `/accounts/resend-code/`
- **Method**: `POST`
- **Request Body**:
  - `email` (string): The user's email address.
- **Response**:
  - `201 Created`: New verification code generated and sent.
  - `200 OK`: An active verification code already exists.
  - `400 Bad Request`: Invalid data.

## Signals

### Create Verification Token

This signal is triggered when a new user account is created. It generates a unique verification code and associates it with the user account.

### Send by Email

This signal is triggered when a new verification token is created. It sends an email to the user containing a link to verify their account, including the unique verification code.

## Celery Beat Tasks

### Delete Expired Codes

This task runs periodically and is responsible for deleting expired verification codes from the database.

### Delete Deactivated Users

This task runs periodically and is responsible for removing deactivated users who haven't verified their accounts within the last 24 hours.

## Custom Manager Methods

### Verify

The `verify` method checks if a given verification code is valid and not expired.

### Re-generate

The `re_generate` method generates a new verification code if the user does not have a valid code.

## Utils

### Generate Unique Verification Code

The `generate_unique_verification_code` utility function generates a unique verification code for a user.

## Exceptions

### DuplicateUserException

This exception is raised when an attempt is made to create a new user account with an email that already has an active user associated with it.

### PendingVerificationException

This exception is raised when an attempt is made to create a new user account with an email that already has a pending verification.

### AlreadyVerifiedException

This exception is raised when an attempt is made to verify an email address that is already verified.

### DuplicationVerificationCodeException

This exception is raised when attempting to resend a verification code while an active code already exists.

## Tests

The tests for the Accounts application can be found in the `pytest apps/accounts` directory.

Run them with following command

```
pytest apps/accounts
```