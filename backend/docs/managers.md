# Managers Application Documentation

The Managers application is responsible for managing managers and their permissions within the Academy Master project. It provides the necessary models, views, and utilities to manage managers and their associated permissions.

## Table of Contents

1. [Models](#models)
    - [Manager](#manager)
2. [Custom Managers](#custom-managers)
    - [ManagerManager](#managermanager)
3. [Permissions](#permissions)
    - [IsManager](#ismanager)
    - [CanAddManager](#canaddmanager)
    - [CanDeleteManager](#candelete_manager)
    - [CanChangeManager](#canchange_manager)
4. [Signals](#signals)
    - [Send Manager Promotion Email](#send-manager-promotion-email)
5. [Views](#views)
    - [ManagerCreateView](#managercreateview)
    - [ManagerUpdateView](#managerupdateview)
    - [ManagerDeleteView](#managerdeleteview)
    - [ManagerRetrieveView](#managerretrieveview)
    - [ManagerListView](#managerlistview)
6. [Tests](#tests)

## Models

### Manager

The `Manager` model represents a manager within the Academy Master project. It contains the following fields:

- `user`: A foreign key relationship to the associated `Account` model.
- `promoted_by`: A foreign key relationship to the `Account` model of the user who promoted the manager.
- `promotion_date`: A datetime field representing the date the manager was promoted.

## Custom Managers

### ManagerManager

A custom manager for adding/updating permissions. It includes the following methods:

- `create_with_permissions()`: Creates a manager with the specified permissions.
- `update_permission()`: Updates a manager's permissions by removing all permissions of a certain class and adding new ones.

## Permissions

### IsManager

This permission allows managers and admins to access specific pages.

### CanAddManager

Only admins and managers with the `can_promote` permission can access the page.

### CanDeleteManager

This permission requires the `can_delete` permission.

### CanChangeManager

This permission requires the `can_change` permission.

## Signals

### Send Manager Promotion Email

This signal is triggered when a new manager is created. It sends an email to the new manager notifying them of their promotion.

## Views

### ManagerCreateView

This view is responsible for creating new managers. It accepts a POST request containing the user's email and permission levels. Response codes include:

- `201`: OK
- `400`: Invalid data
- `403`: Permission denied
- `404`: Not found

### ManagerUpdateView

This view is responsible for updating an existing manager's permission levels. It accepts a PUT/PATCH request containing the user's email and updated permission levels. Response codes include:

- `200`: OK
- `400`: Invalid data
- `403`: Permission denied
- `404`: Not found

### ManagerDeleteView

This view is responsible for deleting a manager. It accepts a DELETE request containing the manager's email. Response codes include:

- `200`: OK
- `403`: Permission denied
- `404`: Not found

### ManagerRetrieveView

This view is responsible for retrieving a manager's details. It accepts a GET request containing the manager's email. Response codes include:

- `200`: OK
- `403`: Permission denied
- `404`: Not found

### ManagerListView

This view is responsible for listing all managers and their associated permissions. Response codes include:

- `200`: OK
- `403`: Permission denied

## Tests

This application is well-tested. To run the tests for the Managers application, use the following command:

```
pytest apps/managers/
```