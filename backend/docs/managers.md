# Managers Application Documentation

## Introduction

The Managers application is responsible for managing managers and their permissions within the Academy Master project. It provides the necessary models, views, and utilities to manage managers and their associated permissions.

## Table of Contents
- [Models](#models)
  - [Manager](#manager)
- [Custom Model Manager](#custom-model-manager)
  - [ManagerManager](#managermanager)
- [Signals](#signals)
  - [Send Manager Promotion Email](#send-manager-promotion-email)
- [Views](#views)
  - [ManagerCreateView](#managercreateview)
  - [ManagerUpdateView](#managerupdateview)
  - [ManagerDeleteView](#managerdeleteview)
  - [ManagerRetrieveView](#managerretrieveview)
  - [ManagerListView](#managerlistview)
- [Permissions](#permissions)
  - [CanAddManager](#canaddmanager)
  - [CanDeleteManager](#candeletemanager)
  - [CanChangeManager](#canchangemanager)
- [Tests](#tests)

## Models

### Manager

The `Manager` model represents a manager within the project. It contains the following fields and methods:

- `user`: A one-to-one field to the associated `Account` model.
- `promoted_by`: A foreign key relationship to the `Account` model of the user who promoted the manager.
- `promotion_date`: A datetime field representing the date the manager was promoted.
- `_validate_creator()`: A method from `AbstractPermission` which ensures that the user who created the manager has permission to promote managers.
- `delete()`: Django Delete method which also removes all user permissions after demoting.

## Custom Model Manager

### ManagerManager

A custom model manager for adding/updating permissions. It includes the following methods:

- `create_with_permissions()`: A method that takes a list of permission objects/codenames and adds them to the manager's permissions.
- `update_permission()`: Updates a manager's permissions by removing all permissions of a certain class and adding new ones.

## Signals

### Send Manager Promotion Email

The `send_manager_promotion_email` signal is triggered when a new manager is created. It sends an email to the new manager notifying them of their promotion.

## Views

### ManagerCreateView

This view is responsible for creating new managers. It accepts a POST request containing the user's email and permission levels. Response codes include:

- `201`: OK
- `400`: Invalid data
- `401`: Unauthorized
- `403`: Permission denied for promoting

### ManagerUpdateView

This view is responsible for updating an existing manager's permission levels. It accepts a PUT/PATCH request containing the user's email and updated permission levels. Response codes include:

- `200`: OK
- `400`: Invalid data
- `401`: Unauthorized
- `403`: Permission denied for promoting
- `404`: Not found

### ManagerRetrieveView

This view is responsible for retrieving a manager's details. It accepts a GET request containing the manager's email. Response codes include:

- `200`: OK
- `401`: Unauthorized
- `403`: Permission denied
- `404`: Not found

### ManagerDeleteView

This view is responsible for deleting a manager. It accepts a DELETE request containing the manager's email. Response codes include:

- `204`: OK
- `401`: Unauthorized
- `403`: Permission denied
- `404`: Not found


### ManagerListView

This view is responsible for listing all managers and their associated permissions. Only managers can access this page. Response codes include:

- `200`: OK
- `401`: Unauthorized
- `403`: Permission denied

## Permissions

### CanAddManager

This permission checks if the user is a manager and has the `add_manager` permission for adding a manager.

### CanDeleteManager

This permission checks if the user is a manager and has the `delete_manager` permission for deleting a manager.

### CanChangeManager

This permission checks if the user is a manager and has the `change_manager` permission for updating a manager.

## Tests

The tests for the Managers application can be found in the `apps/managers` directory.

Run them with the following command:

```
pytest apps/managers/
```