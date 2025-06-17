# Validation Documentation: sample

## CrossFileUtils.java
## CrossFileUtils

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | int | 0 |  |  |  | Age cannot be negative |


## User.java
## User

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name |  | String |  |  |  |  |  |
| age |  | int | 0 |  |  |  |  |


## app.js
## User

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes | text |  |  |  |  |  |
| age | Yes | number | 18 |  |  |  |  |
| email | Yes | email |  |  | Yes |  |  |


## cross_file_main.java
## Person

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be a non-negative integer |


## CrossFileUtils (Inferred from usage)

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  |  |


## decorator.py
## UserModel

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| email |  | str |  |  | ✓ |  | must contain @ |
| age |  | int | 0 |  |  |  | must be positive |


## dynamic_fields.py
## DynamicUser

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age |  |  | 0 |  |  |  | Must be positive |

> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete.


## validations.java
## AdvancedValidationCar

| Field             | Required | Type      | Min     | Max      | Email | Pattern                     | Positive | PositiveOrZero | Negative | NegativeOrZero | Past             | PastOrPresent   | Future            | FutureOrPresent | DecimalMin | DecimalMax      | Digits (integer/fraction) | AssertTrue | AssertFalse | Size (min/max) | Other Validation |
|----------------------|----------|-----------|---------|----------|-------|-----------------------------|----------|-----------------|----------|-----------------|-----------------|-----------------|-------------------|-------------------|------------|-----------------|--------------------------|------------|-------------|-----------------|-----------------|
| vin                | Yes      | String    |         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| ownerName          | Yes      | String    |         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| licensePlate       |          | String    |         |          |       | [A-Z]{2}[0-9]{2} [A-Z]{3} |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| year               |          | int       | 1886    | 2100     |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| modelName          |          | String    |         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             | 2/30             |                 |
| contactEmail       |          | String    |         |          | Yes   |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| numberOfDoors      |          | int       |         |          |       |                             | Yes      |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| numberOfPreviousOwners |          | int       |         |          |       |                             |          | Yes              |          |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| negativeTestValue  |          | int       |         |          |       |                             |          |                 | Yes      |                 |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| negativeOrZeroTestValue |          | int       |         |          |       |                             |          |                 |          | Yes              |                 |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| registrationDate   |          | LocalDate |         |          |       |                             |          |                 |          |                 | Yes             |                 |                 |                 |            |                 |                          |            |             |                 |                 |
| lastServiceDate    |          | LocalDate |         |          |       |                             |          |                 |          |                 |                 | Yes              |                 |                 |            |                 |                          |            |             |                 |                 |
| insuranceExpiryDate |          | LocalDate |         |          |       |                             |          |                 |          |                 |                 |                 | Yes             |                 |            |                 |                          |            |             |                 |                 |
| warrantyExpiryDate  |          | LocalDate |         |          |       |                             |          |                 |          |                 |                 |                 |                 | Yes              |            |                 |                          |            |             |                 |                 |
| price              |          | BigDecimal|         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 | 0.0         | 1000000.0      |                          |            |             |                 |                 |
| engineCapacity     |          | BigDecimal|         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 | 5/2                     |            |             |                 |                 |
| isInsured          |          | boolean   |         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          | Yes         |             |                 |                 |
| isStolen           |          | boolean   |         |          |       |                             |          |                 |          |                 |                 |                 |                 |                 |            |                 |                          |            | Yes          |                 |                 |


## validations.py
## User

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes | str |  |  |  |  | Cannot be empty |
| age | Yes | int | 18 |  |  |  |  |
| email | Yes | str |  |  | Yes |  | Must contain "@" symbol |
