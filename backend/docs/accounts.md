# Accounts Application Documentation

The Accounts application is responsible for user authentication and verification within the Academy Master project. It provides the necessary models, views, and utilities to manage user accounts and their associated verification codes.

## Table of Contents

1. [Models](#models)
    - [Account](#account)
    - [VerificationCode](#verificationcode)
2. [Views](#views)
    - [Register](#register)
    - [Verify](#verify)
    - [Token](#token)
3. [Signals](#signals)
    - [Create Verification Token](#create-verification-token)
    - [Send by Email](#send-by-email)
4. [Celery Beat Tasks](#celery-beat-tasks)
    - [Delete Expired Codes](#delete-expired-codes)
    - [Delete Deactivate Users](#delete-deactivate-users)
5. [Custom Manager Methods](#custom-manager-methods)
    - [Verify](#verify)
    - [Check or Create](#check-or-create)
6. [Utils](#utils)
    - [Generate Unique Verification Code](#generate-unique-verification-code)
7. [Exceptions](#exceptions)
    - [DuplicateUserException](#duplicateuserexception)
    - [PendingVerificationException](#pendingverificationexception)
    - [AlreadyVerifiedException](#alreadyverifiedexception)
    - [InvalidVerificationCodeException](#invalidverificationcodeexception)
8. [Tests](#tests)

## Models

### Account

The `Account` model represents a user account. It contains the following fields:

- `email`: A unique email address for the user.
- `password`: A hashed password for the user.
- `is_active`: A boolean flag indicating if the user's account is active.
- `first_name`: A String field that saves user's first_name.
- `last_name`: An Optional String field that saves user's last_name.

### VerificationCode

The `VerificationCode` model represents a unique code associated with a user account for the purpose of email verification. It contains the following fields:

- `code`: A unique alphanumeric string representing the verification code.
- `user`: A foreign key relationship to the associated `Account` model.
- `expiration_date`: A datetime field representing the expiration date of the verification code.
- `retry_count`: An int field that saves the retries of a verification code.

## Views

### Register

The `Register` view is responsible for handling user registration. It accepts a POST request containing the user's email and password. Upon successful registration, a verification token is created and sent to the user's email.

### Verify

The `Verify` view is responsible for handling email verification. It accepts a POST request containing a verification code. If the code is valid and not expired, the associated user account's `is_active` field is set to `True`.

### Token

The `Token` view is responsible for handling authentication and generating tokens. It accepts a POST request containing a user's email and password. If the credentials are valid and the user's email has been verified, a JWT token is generated and returned in the response.

## Signals

### Create Verification Token

This signal is triggered when a new user account is created. It generates a unique verification code and associates it with the user account.

### Send by Email

This signal is triggered when a new verification token is created. It sends an email to the user containing a link to verify their account, including the unique verification code.

## Celery Beat Tasks

### Delete Expired Codes

This task is scheduled to run periodically and is responsible for deleting expired verification codes from the database.

### Delete Deactivate Users

This task is scheduled to run periodically and is responsible for removing deactivated users that hasnt verified within last 24 hours.


## Custom Manager Methods

### Verify

The `verify` method checks if a given verification code is valid and not expired. If the code is valid.

### Check or Create

The `check_or_create` method checks if a user account has a valid verification code. If not, it generates a new code and sends it to the user's email.

## Utils

### Generate Unique Verification Code

The `generate_unique_verification_code` utility function generates a unique alphanumeric verification code for a user.

## Exceptions

### DuplicateUserException

Raised when an attempt is made to create a new user account with an email that already has an active user associated with it. Returns a 400 Bad Request response.

### PendingVerificationException

Raised when an attempt is made to create a new user account with an email that already has a pending verification. Returns a 200 OK response to prompt the user to complete the verification process.

### AlreadyVerifiedException

Raised when an attempt is made to verify an email address that has already been verified. Returns a 409 Conflict response.

### InvalidVerificationCodeException

Raised when a submitted verification token is either invalid or expired. Returns a 400 Bad Request response.

## Tests
This application is well-tested. <br>
To run the tests for the Accounts application, use the following command:

```
pytest apps/accounts/
```