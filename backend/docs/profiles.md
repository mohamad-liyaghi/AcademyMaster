# Profiles Application Documentation

## Introduction

The Profiles application is responsible for handling user profiles within the Academy Master project. After a user creates an account, a profile object is created for them. The profile object contains additional information about the user, such as their profile picture, date of birth, and phone number.

## Table of Contents
- [Models](#models)
  - [Profile](#profile)
- [Signals](#signals)
  - [Create Profile for Active User](#create-profile-for-active-user)
- [Views](#views)
  - [Profile Detail](#profile-detail)
  - [Update Profile](#update-profile)
- [Permissions](#permissions)
  - [CanUpdateProfile](#canupdateprofile)
  - [CanRetrieveProfile](#canretrieveprofile)
- [Tests](#tests)

## Models

### Profile

The `Profile` model represents a user profile. It contains the following fields:

- `user`: A one-to-one relationship to the associated `Account` model.
- `avatar`: An optional image field for the user's profile picture.
- `birth_date`: A date field for the user's date of birth.
- `passport_id`: A char field for saving users passport id.
- `phone_number`: A char field that only accepts numbers with IR pattern.
- `age`: A property that extracts age from the user's birth date.
- `__check_required_fields()`: A method that checks if all the data fields are filled.

## Signals

### Create Profile for Active User

The `create_profile_for_active_user` signal is triggered when a new user account is activated (i.e., email verification is complete). It creates a new profile associated with the activated user account.

## Views

### Profile Detail

The `ProfileRetrieveView` is responsible for displaying a user's profile information. This view is accessible only to the profile owner and users with the `teacher` or `manager` role.

### Update Profile

The `ProfileUpdateView` is responsible for handling updates to a user's profile information. Only the profile owner can update their profile.

## Permissions

### CanUpdateProfile

Make sure that the requesting user is the profile owner.

### CanRetrieveProfile

Make sure that the requesting user is the profile owner or has the `teacher` or `manager` role.

## Tests

The tests for the Profiles application can be found in the `apps/profiles` directory.

Run them with the following command:

```
pytest apps/profiles/
```