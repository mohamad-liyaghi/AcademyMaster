# Managers Application Documentation

The Managers application is responsible for managing managers and thier permissions and within the Academy Master project. It provides the necessary models, views, and utilities to manage managers and their associated permissions.

## Table of Contents

1. [Models](#models)
    - [Manager](#manager)
2. [Custom Managers](#custom-managers)
    - [ManagerManager](#managermanager)
3. [Signals](#signals)
    - [Send Email Notification](#send-email-notification)
4. [Permissions](#permissions)
    - [IsManager](#ismanager)
    - [CanPromotePermission](#canpromotepermission)
    - [CanDemotePermission](#candemotepermission)
    - [IsManagerPromoter](#ismanagerpromoter)
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

A custom manager for for adding/updating permissions .

## Signals

### Send Email Notification

This signal is triggered when a new manager is created. It sends an email to the new manager notifying them of their promotion.

## Permissions

### IsManager

This permission allows managers and admins to access specific pages.

### CanPromotePermission

This permission allows admins/managers who can promote managers to access specific pages.

### CanDemotePermission

This permission allows admins/managers who can demote managers to access specific pages.

### IsManagerPromoter

This permission allows admins and the manager's promoter to access specific pages.

## Views

### ManagerCreateView

This view is responsible for creating new managers. It accepts a POST request containing the user's email and permission levels.

### ManagerUpdateView

This view is responsible for updating an existing manager's permission levels. It accepts a PUT/PATCH request containing the user's email and updated permission levels.

### ManagerDeleteView

This view is responsible for deleting a manager. It accepts a DELETE request containing the manager's email.

### ManagerRetrieveView

This view is responsible for retrieving a manager's details. It accepts a GET request containing the manager's email.

### ManagerListView

This view is responsible for listing all managers and their associated permissions.

## Tests

This application is well-tested. To run the tests for the Managers application, use the following command:

```
pytest apps/managers/
```