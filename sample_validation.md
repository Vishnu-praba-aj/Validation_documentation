# Validation Documentation: sample

## CrossFileUtils.java
## CrossFileUtils

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| age | int |  | 0 |  |  |


## User.java
## User

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| name | String |  |  |  |  |
| age | int |  | 0 |  | Must be non-negative |


## app.js
## UserController

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| name | String |  |  |  |  |
| age | Number |  |  |  |  |
| email | String |  |  |  |  |


## cross_file_main.java
## Person

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| age | int |  | 0 |  |  |


## CrossFileUtils (Inferred from usage)

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| age (input parameter) | int |  | 0 |  |  |


## decorator.py
## UserModel

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| email | str |  |  |  | must contain @ |
| age | int |  | 0 |  | must be positive |


## dynamic_fields.py
## DynamicUser

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| age |  | ✓ | 0 |  |  Must be positive |

> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete.


## js_dynamic.js
## DynamicObj

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| field_`Math.random()` | Number |  |  |  | Assigned dynamically; value is 42 |
| `name` (set via `setField`) | Any |  |  |  | Set dynamically via `setField` method |
| `value` (set via `setField`) | Any |  |  |  | Set dynamically via `setField` method |


## validations.java
## AdvancedValidationCar

| Field             | Type      | Required | Min     | Max      | Pattern                     | Email     | Positive | PositiveOrZero | Negative | NegativeOrZero | Past          | PastOrPresent | Future         | FutureOrPresent | DecimalMin   | DecimalMax     | Digits (integer/fraction) | AssertTrue | AssertFalse | Size (min/max) |
|----------------------|------------|----------|----------|-----------|-----------------------------|------------|----------|-----------------|----------|-----------------|---------------|---------------|-----------------|-----------------|---------------|-----------------|-------------------------|-------------|-------------|-----------------|
| vin                 | String    | ✓        |          |           |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| ownerName           | String    | ✓        |          |           |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| licensePlate        | String    |          |          |           | [A-Z]{2}[0-9]{2} [A-Z]{3} |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| year                | int       |          | 1886     | 2100      |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| modelName           | String    |          |          |           |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             | 2/30           |
| contactEmail        | String    |          |          |           |                             | ✓         |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| numberOfDoors       | int       |          |          |           |                             |            | ✓        |                 |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| numberOfPreviousOwners | int       |          |          |           |                             |            |          | ✓               |          |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| negativeTestValue   | int       |          |          |           |                             |            |          |                 | ✓        |                 |               |               |                 |                 |               |                 |                         |             |             |                 |
| negativeOrZeroTestValue | int       |          |          |           |                             |            |          |                 |          | ✓               |               |               |                 |                 |               |                 |                         |             |             |                 |
| registrationDate    | LocalDate  |          |          |           |                             |            |          |                 |          |                 | ✓           |               |                 |                 |               |                 |                         |             |             |                 |
| lastServiceDate     | LocalDate  |          |          |           |                             |            |          |                 |          |                 |               | ✓           |                 |                 |               |                 |                         |             |             |                 |
| insuranceExpiryDate | LocalDate  |          |          |           |                             |            |          |                 |          |                 |               |               | ✓           |                 |               |                 |                         |             |             |                 |
| warrantyExpiryDate  | LocalDate  |          |          |           |                             |            |          |                 |          |                 |               |               |                 | ✓               |               |                 |                         |             |             |                 |
| price               | BigDecimal |          |          |           |                             |            |          |                 |          |                 |               |               |                 |                 | 0.0          | 1000000.0      |                         |             |             |                 |
| engineCapacity      | BigDecimal |          |          |           |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 | 5/2                     |             |             |                 |
| isInsured           | boolean   |          |          |           |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         | ✓           |             |                 |
| isStolen            | boolean   |          |          |           |                             |            |          |                 |          |                 |               |               |                 |                 |               |                 |                         |             | ✓           |                 |


## DynamicCar

No statically analyzable validation logic present.


## validations.py
## User

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| name | str | True |  |  | Cannot be empty |
| age | int | True | 18 |  |  |
| email | str | True |  |  | Must contain "@" symbol |
