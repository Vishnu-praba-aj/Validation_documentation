# Validation Documentation: sample

## User.java
## User

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| name | String |  |  |  |  |
| age | int |  | 0 |  | Must be non-negative |


## cross_file_main.java
## Person

| Field | Type | Required | Min | Max | Other Validation |
| :------------------ | :--------------- | :-------- | :-: | :-: | :----------------- |
| age |  | ✓ |  |  | Must pass `cross_file_utils.validate_age` |


## cross_file_utils.java
## cross_file_utils

| Field | Type | Required | Min | Max | Other Validation |
| :---------- | :---------- | :---------- | :---------- | :---------- | :---------- |
| age |  |  | 0 |  | Must be non-negative |


## decorator_validation.py
## UserModel

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| email | str |  |  |  | must contain @ |
| age | int |  | 0 |  | must be positive |


## dynamic_fields.py
## DynamicUser

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| age |  | ✓ | 0 |  |  |

> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete.



## js_dynamic.js
## DynamicObj

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| field_*(dynamic)* | Number |  |  |  | Assigned a random key during construction, value is 42 |
| *(dynamic)* | *varies* |  |  |  | Set dynamically using `setField` method; no inherent type or range restrictions |


## test.py
## `register_user` function

| Field | Type | Required | Min | Max | Other Validation |
|---|---|---|---|---|---|
| name | str | True |  |  | Cannot be empty |
| age | int |  | 18 |  | Must be at least 18 |
| email | str |  |  |  | Must contain "@" symbol |


## validations.java
## AdvancedValidationCar

| Field             | Type          | Required | Min     | Max      | Pattern                     | Email     | Positive | PositiveOrZero | Negative | NegativeOrZero | Past              | PastOrPresent     | Future             | FutureOrPresent    | DecimalMin | DecimalMax      | Digits      | AssertTrue | AssertFalse | Size Min | Size Max |
|----------------------|---------------|----------|---------|----------|-----------------------------|-----------|----------|-----------------|----------|-----------------|-----------------|--------------------|--------------------|--------------------|-------------|-----------------|--------------|-------------|-------------|----------|----------|
| vin                | String        | ✓        |         |          |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              | ✓           |             |          |          |
| ownerName          | String        | ✓        |         |          |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| licensePlate       | String        |          |         |          | `[A-Z]{2}[0-9]{2} [A-Z]{3}` |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| year               | int           |          | 1886    | 2100     |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| modelName          | String        |          |         |          |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              |             |             | 2         | 30        |
| contactEmail       | String        |          |         |          |                             | ✓         |          |                 |          |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| numberOfDoors      | int           |          |         |          |                             |           | ✓        |                 |          |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| numberOfPreviousOwners | int           |          |         |          |                             |           |          | ✓                |          |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| negativeTestValue   | int           |          |         |          |                             |           |          |                 | ✓        |                 |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| negativeOrZeroTestValue | int           |          |         |          |                             |           |          |                 |          | ✓                |                 |                    |                 |                    |             |                 |              |             |             |          |          |
| registrationDate   | LocalDate     |          |         |          |                             |           |          |                 |          |                 | ✓                |                    |                 |                    |             |                 |              |             |             |          |          |
| lastServiceDate    | LocalDate     |          |         |          |                             |           |          |                 |          |                 |                 | ✓                   |                 |                    |             |                 |              |             |             |          |          |
| insuranceExpiryDate | LocalDate     |          |         |          |                             |           |          |                 |          |                 |                 |                    | ✓                |                    |             |                 |              |             |             |          |          |
| warrantyExpiryDate  | LocalDate     |          |         |          |                             |           |          |                 |          |                 |                 |                    |                 | ✓                   |             |                 |              |             |             |          |          |
| price              | BigDecimal    |          | 0.0      | 1000000.0 |                             |           |          |                 |          |                 |                 |                    |                 |                    | ✓           | ✓               |              |             |             |          |          |
| engineCapacity     | BigDecimal    |          |         |          |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 | ✓            |             |             |          |          |
| isInsured          | boolean       |          |         |          |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              | ✓           |             |          |          |
| isStolen           | boolean       |          |         |          |                             |           |          |                 |          |                 |                 |                    |                 |                    |             |                 |              |             | ✓           |          |          |


## DynamicCar

No statically analyzable validation logic is present in this class.
