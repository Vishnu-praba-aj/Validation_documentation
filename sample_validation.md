# Validation Documentation: sample

## CrossFileUtils.java
## CrossFileUtils

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | int | 0 |  |  |  | Must not be negative |


## User.java
## User

| Field | Required | Type     | Min | Max | Default | Pattern | Other Validation                     |
|-------|----------|----------|-----|-----|---------|---------|--------------------------------------|
| name  |          | String   |     |     |         |         |                                      |
| age   |          | Integer  | 0   |     |         |         | Must be non-negative (age >= 0)     |


## app.js
## User

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes | text |  |  | '' |  |  |
| age | Yes | number | 18 |  | null |  |  |
| email | Yes | email |  |  | '' |  |  |


## `userForm` (AngularJS Form)

This table represents the validation enforced by the AngularJS form itself,  as indicated by the `ng-show` directives and `ng-disabled` attribute in the HTML.  It reflects the client-side validation.

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation (AngularJS) |
|---|---|---|---|---|---|---|---|
| name | Yes (`required`) | text |  |  |  |  | `userForm.name.$dirty && userForm.name.$error.required` |
| age | Yes (`required`) | number | 18 (`min="18"`) |  |  |  | `userForm.age.$dirty && userForm.age.$error.required`, `userForm.age.$dirty && userForm.age.$error.min` |
| email | Yes (`required`) | email |  |  |  |  | `userForm.email.$dirty && userForm.email.$error.required`, `userForm.email.$dirty && userForm.email.$error.email` |


## `UserController` (AngularJS Controller)

This table represents the server-side validation implied by the controller's `register` function.  This is a simplified representation as more robust server-side checks would typically be present in a real-world application.

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation (Server-Side Implied) |
|---|---|---|---|---|---|---|---|
| name | Yes (Implied) |  |  |  |  |  | Validation occurs only if `$scope.userForm.$valid` is true. |
| age | Yes (Implied) |  |  |  |  |  | Validation occurs only if `$scope.userForm.$valid` is true. |
| email | Yes (Implied) |  |  |  |  |  | Validation occurs only if `$scope.userForm.$valid` is true. |

**Note:** The server-side validation in `app.js` is minimal.  A production system would require far more extensive server-side checks to ensure data integrity and security (e.g., database constraints, uniqueness checks, input sanitization).  The table above reflects only the implicit validation based on the provided code.


## cross_file_main.java
## Person

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be a non-negative integer. |


## CrossFileUtils (Inferred from Usage)

CrossFileUtils is not directly examined, but its `validateAge` method is used.  We infer its validation based on the exception thrown in `CrossFileMain`.

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be non-negative; throws IllegalArgumentException if not. |


## decorator.py
## UserModel

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| email | True | str |  |  |  |  | must contain @ |
| age | True | int | 0 |  |  |  | must be positive |


## dynamic_fields.py
## DynamicUser

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age |  |  | 0 |  |  |  | Must be positive |

> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete.


## validations.java
## AdvancedValidationCar

| Field             | Required | Type             | Min     | Max      | Default | Pattern                     | Email      | Positive | PositiveOrZero | Negative | NegativeOrZero | Past             | PastOrPresent    | Future            | FutureOrPresent   | DecimalMin     | DecimalMax       | Digits (integer/fraction) | AssertTrue | AssertFalse | Other Validation |
|----------------------|----------|-----------------|---------|----------|---------|-----------------------------|------------|----------|-----------------|----------|-----------------|-----------------|-------------------|-----------------|-------------------|-----------------|-------------------|------------------------|-------------|-------------|-------------------|
| vin                | Yes      | String           |         |          |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@NotNull`       |
| ownerName          | Yes      | String           |         |          |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@NotBlank`      |
| licensePlate       |          | String           |         |          |         | `[A-Z]{2}[0-9]{2} [A-Z]{3}` |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@Pattern`       |
| year               |          | int              | 1886    | 2100     |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@Min`, `@Max`    |
| modelName          |          | String           | 2       | 30       |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@Size`          |
| contactEmail       |          | String           |         |          |         |                             | Yes        |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@Email`         |
| numberOfDoors      |          | int              |         |          |         |                             |            | Yes      |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@Positive`      |
| numberOfPreviousOwners |          | int              |         |          |         |                             |            |          | Yes              |          |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@PositiveOrZero` |
| negativeTestValue  |          | int              |         |          |         |                             |            |          |                 | Yes      |                 |                 |                   |                 |                   |                 |                 |                        |             |             | `@Negative`      |
| negativeOrZeroTestValue |          | int              |         |          |         |                             |            |          |                 |          | Yes              |                 |                   |                 |                   |                 |                 |                        |             |             | `@NegativeOrZero`|
| registrationDate   |          | LocalDate        |         |          |         |                             |            |          |                 |          |                 | Yes             |                   |                 |                   |                 |                 |                        |             |             | `@Past`          |
| lastServiceDate    |          | LocalDate        |         |          |         |                             |            |          |                 |          |                 |                 | Yes                |                 |                   |                 |                 |                        |             |             | `@PastOrPresent` |
| insuranceExpiryDate |          | LocalDate        |         |          |         |                             |            |          |                 |          |                 |                 |                   | Yes             |                   |                 |                 |                        |             |             | `@Future`        |
| warrantyExpiryDate  |          | LocalDate        |         |          |         |                             |            |          |                 |          |                 |                 |                   |                 | Yes                |                 |                 |                        |             |             | `@FutureOrPresent`|
| price              |          | BigDecimal       | 0.0     | 1000000.0 |         |                             |            |          |                 |          |                 |                 |                   |                 |                   | 0.0             | 1000000.0       |                        |             |             | `@DecimalMin`, `@DecimalMax` |
| engineCapacity     |          | BigDecimal       |         |          |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 | 5/2                    |             |             | `@Digits`        |
| isInsured          |          | boolean          |         |          |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        | Yes           |             | `@AssertTrue`    |
| isStolen           |          | boolean          |         |          |         |                             |            |          |                 |          |                 |                 |                   |                 |                   |                 |                 |                        |             | Yes           | `@AssertFalse`   |


## validations.py
## User

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes | str |  |  |  |  | Cannot be empty |
| age | Yes | int | 18 |  |  |  | Must be at least 18 years old |
| email | Yes | str |  |  |  | Contains "@" symbol |  |
