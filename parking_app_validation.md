# Validation Documentation: parking_app

## User

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation             |
|-------------|----------|---------|-----|-----|---------|---------|-----------------------------|
| name       | Yes      | String  |     |     |         |         |                             |
| age        | Yes      | Integer | 0   |     |         |         | Must be positive             |
| email      | Yes      | String  |     |     |         | @       | Must contain "@" symbol     |
| password   | Yes      | String  | 8   |     |         |         | Minimum length validation     |



## Admin

| Field          | Required | Type    | Min | Max | Default | Pattern | Other Validation             |
|-----------------|----------|---------|-----|-----|---------|---------|-----------------------------|
| name           | Yes      | String  |     |     |         |         |                             |
| age            | Yes      | Integer | 0   |     |         |         | Must be positive             |
| email          | Yes      | String  |     |     |         | @       | Must contain "@" symbol     |
| access_level   | Yes      | Integer | 1   | 10  |         |         | Must be between 1 and 10     |



## Car

| Field         | Required | Type    | Min       | Max | Default | Pattern | Other Validation             |
|----------------|----------|---------|------------|-----|---------|---------|-----------------------------|
| licensePlate  | Yes      | String  | 5          |     |         |         | Minimum length 5 characters |
| year          | Yes      | Integer | 1886       |     |         |         | Must be >= 1886              |



## Product

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation             |
|-------------|----------|---------|-----|-----|---------|---------|-----------------------------|
| name       | Yes      | String  |     |     |         |         |                             |
| price      | Yes      | Number  | 0   |     |         |         | Must be non-negative          |



## Inventory

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation             |
|-------------|----------|---------|-----|-----|---------|---------|-----------------------------|
| item.name  | Yes      | String  |     |     |         |         | Item and its name are required |



## Person

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation             |
|-------------|----------|---------|-----|-----|---------|---------|-----------------------------|
| age        | Yes      | Integer | 0   |     |         |         | Must be non-negative          |

## No Specific Entities Found for Validation

The provided code only contains a single function, `validate_age`, which performs age validation.  There are no classes or objects with fields to validate. Therefore, a table summarizing field-level validation rules cannot be created.  The `validate_age` function's logic is summarized below.


| Function | Parameter | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| `validate_age` | `age` | Yes | Integer | 0 |  |  |  | Must be non-negative |


The `validate_age` function raises a `ValueError` if the input `age` is negative.  This is captured in the "Other Validation" column.  No other validation logic is present in the provided code.

## UserModel

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| email | True | str |  |  |  |  | must contain @ |
| age | True | int | 0 |  |  |  | must be positive |

## DynamicUser

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation             |
|-------------|----------|---------|-----|-----|---------|---------|---------------------------------|
| age        | No       | Integer | 0   |     |         |         | Must be positive (if field exists) |
| *dynamic*  | No       | Varies  |     |     |         |         |  Validation depends on the field name and value. |

**Note:** The `DynamicUser` class allows for dynamic field creation, so a comprehensive table listing all potential fields and their validation rules is not possible. The table above includes validation for the `age` field (if it exists) and a row for dynamic fields, noting the dynamic nature of the validation.

## AdvancedValidationCar

| Field             | Required | Type          | Min      | Max      | Default | Pattern                 | Email      | Positive | PositiveOrZero | Negative | NegativeOrZero | Past           | PastOrPresent | Future          | FutureOrPresent | DecimalMin | DecimalMax    | Digits (integer,fraction) | AssertTrue | AssertFalse | Size (min,max) | Other Validation |
|----------------------|----------|---------------|----------|----------|---------|--------------------------|------------|----------|-----------------|----------|-----------------|-----------------|-----------------|-----------------|-----------------|-------------|----------------|--------------------------|-------------|-------------|-----------------|--------------------|
| vin                | Yes      | String        |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| ownerName          | Yes      | String        |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| licensePlate       | No       | String        |          |          |         | [A-Z]{2}[0-9]{2} [A-Z]{3} |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| year               | No       | int           | 1886     | 2100     |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| modelName          | No       | String        |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             | 2, 30            |                    |
| contactEmail       | No       | String        |          |          |         |                          | Yes        |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| numberOfDoors      | No       | int           |          |          |         |                          |            | Yes      |                 |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| numberOfPreviousOwners | No       | int           |          |          |         |                          |            |          | Yes              |          |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| negativeTestValue  | No       | int           |          |          |         |                          |            |          |                 | Yes      |                 |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| negativeOrZeroTestValue | No       | int           |          |          |         |                          |            |          |                 |          | Yes              |                 |                 |                 |                 |             |                |                          |             |             |                 |                    |
| registrationDate   | No       | LocalDate     |          |          |         |                          |            |          |                 |          |                 | Yes           |                 |                 |                 |             |                |                          |             |             |                 |                    |
| lastServiceDate    | No       | LocalDate     |          |          |         |                          |            |          |                 |          |                 |                 | Yes              |                 |                 |             |                |                          |             |             |                 |                    |
| insuranceExpiryDate | No       | LocalDate     |          |          |         |                          |            |          |                 |          |                 |                 |                 | Yes           |                 |             |                |                          |             |             |                 |                    |
| warrantyExpiryDate  | No       | LocalDate     |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 | Yes              |             |                |                          |             |             |                 |                    |
| price               | No       | BigDecimal    | 0.0       | 1000000.0 |         |                          |            |          |                 |          |                 |                 |                 |                 |                 | Yes         | Yes            |                          |             |             |                 |                    |
| engineCapacity      | No       | BigDecimal    |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                | 5,2                     |             |             |                 |                    |
| isInsured           | No       | boolean       |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          | Yes          |             |                 |                    |
| isStolen            | No       | boolean       |          |          |         |                          |            |          |                 |          |                 |                 |                 |                 |                 |             |                |                          |             | Yes          |                 |                    |



## DynamicCar

No validation logic is present within the `DynamicCar` class itself.  The `setField` method uses reflection (simulated here), making static analysis of validation impossible.  Therefore, no table is created for this class.

## DynamicObj

| Field        | Required | Type   | Min | Max | Default | Pattern | Other Validation |
|--------------|----------|--------|-----|-----|---------|---------|-----------------|
| `field_*`    |          | Number |     |     | 42      |         | Dynamically named, generated during construction. Value is not validated beyond assignment. |
| Any other field (set via `setField`) |          | Any    |     |     |         |         | No explicit validation; values are assigned directly. |


**Note:** The `DynamicObj` class lacks explicit validation rules.  Field names are dynamically generated, and values are set without type checking or range limitations.  The "Other Validation" column highlights the dynamic nature of field names and the absence of other constraints.

## Login

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation                               |
|------------|----------|---------|-----|-----|---------|---------|---------------------------------------------------|
| username   | Yes      | String  |     |     |         |         | Must exist in the database                     |
| password   | Yes      | String  |     |     |         |         | Must match the password in the database        |

## ParkingLot

| Field                | Required | Type             | Min     | Max       | Default | Pattern | Other Validation                                           |
|-----------------------|----------|-------------------|---------|-----------|---------|---------|-----------------------------------------------------------|
| prime_location_name | Yes      | String           |         |           |         |         |                                                           |
| price_per_hour       | Yes      | Float/Integer    |         |           |         |         | Must be a positive number                               |
| address              | Yes      | String           |         |           |         |         |                                                           |
| pin_code             | Yes      | String/Integer   |         |           |         |         |                                                           |
| max_number_of_spots  | Yes      | Integer          | 1       |           |         |         | Must be a positive integer. Cannot reduce if spots occupied |



## ParkingSpot

| Field       | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|---------|---------|--------------------|
| lot_id      | Yes      | Integer |     |     |         |         |                   |
| spot_number | Yes      | String  |     |     |         |         |                   |
| status      | Yes      | String  |     |     | 'A'     |         | 'A' for available, 'O' for occupied |



## Reservation

| Field              | Required | Type             | Min   | Max   | Default | Pattern | Other Validation                                     |
|----------------------|----------|-------------------|-------|-------|---------|---------|-----------------------------------------------------|
| spot_id             | Yes      | Integer          |       |       |         |         |                                                     |
| user_id             | Yes      | Integer          |       |       |         |         |                                                     |
| parking_timestamp   | Yes      | DateTime         |       |       |         |         | Automatically set to current UTC time on creation     |
| leaving_timestamp   | No       | DateTime         |       |       |         |         | Automatically set to current UTC time on spot release |
| parking_cost        | No       | Float            | 0     |       | 0       |         | Calculated based on duration and price_per_hour       |



## Booking Request (book_parking_spot)

| Field     | Required | Type    | Min | Max | Default | Pattern | Other Validation                                   |
|-----------|----------|---------|-----|-----|---------|---------|---------------------------------------------------|
| user_id   | Yes      | Integer |     |     |         |         | User ID must exist in the database.             |



## Update Parking Lot Request (update_parking_lot)

| Field                | Required | Type             | Min     | Max       | Default | Pattern | Other Validation                                           |
|-----------------------|----------|-------------------|---------|-----------|---------|---------|-----------------------------------------------------------|
| prime_location_name | No       | String           |         |           |         |         |                                                           |
| price_per_hour       | No       | Float/Integer    |         |           |         |         | Must be a positive number                               |
| address              | No       | String           |         |           |         |         |                                                           |
| pin_code             | No       | String/Integer   |         |           |         |         |                                                           |
| max_number_of_spots  | No       | Integer          | 1       |           |         |         | Must be a positive integer. Cannot reduce if spots occupied |

## Parking Spot

| Field           | Required | Type         | Min     | Max       | Default | Pattern | Other Validation                               |
|-----------------|----------|---------------|----------|------------|---------|----------|-----------------------------------------------|
| id               | Yes      | INTEGER       |          |            |         |          | Must be unique (Primary Key)                 |
| lot_id          | Yes      | INTEGER       |          |            |         |          | Must be a valid foreign key referencing parking_lot |
| spot_number      | Yes      | VARCHAR(10)  |          |            |         |          |                                               |
| status           | Yes      | VARCHAR(1)   |          |            |         |          |  Should be a single character (e.g., 'O' or 'A') |



