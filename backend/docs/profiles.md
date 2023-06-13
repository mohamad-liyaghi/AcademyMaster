# Profiles Application Documentation

The Profiles application is responsible for handling user profiles within the Academy Master project. It provides the necessary models, views, and permissions to manage user profiles and their associated information.

## Table of Contents

1. [Models](#models)
    - [Profile](#profile)
2. [Signals](#signals)
    - [Create Profile for Active User](#create-profile-for-active-user)
3. [Views](#views)
    - [ProfileDetail](#profiledetail)
    - [ProfileUpdate](#profileupdate)
4. [Permissions](#permissions)
    - [IsProfileOwner](#isprofileowner)
    - [IsNonStudent](#isnonstudent)
5. [Tests](#tests)

## Models

### Profile

The `Profile` model represents a user profile. It contains the following fields:

- `user`: A one-to-one relationship to the associated `Account` model.
- `avatar`: An optional image field for the user's profile picture.
- `birth_date`: An optional date field for the user's date of birth.
- `passport_id`: A char field for saving users passport id.
- `phone_number`: A char field that only accepts numbers with IR pattern.
- `age`: A property that extracts age from users birth date.

## Signals

### Create Profile for Active User

This signal is triggered when a new user account is activated (i.e., email verification is complete). It creates a new profile associated with the activated user account.

## Views

### ProfileDetail

The `ProfileDetail` view is responsible for displaying a user's profile information. This view is accessible only to the profile owner and users with the `teacher` or `manager` role.

### ProfileUpdate

The `ProfileUpdate` view is responsible for handling updates to a user's profile information. Only the profile owner can update their profile.


## Permissions

### IsProfileOwner

This permission class checks if the requesting user is the owner of the profile they are trying to access or modify.

### IsNonStudent

This permission class checks if the requesting user has a role other than `student`. This is used to restrict access to certain views for users with the `teacher` or `manager` role.

## Tests

The Profiles application is well-tested. To run the tests for the Profiles application, use the following command:

```
pytest apps/profiles/
```