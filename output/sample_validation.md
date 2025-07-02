# Validation Documentation: sample

## User

| Field | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|---------|-----|-----|--------|---------|---------|------------------|
| name  | Yes      | String  |     |     |        |         |         |                  |
| age   | Yes      | Integer | 0   |     |        |         |         | Must be non-negative |

## app.js

| Field | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|---------|-----|-----|--------|---------|---------|------------------|
| name  | Yes      | String  |     |     |        |         |         |                  |
| age   | Yes      | Number  | 18  |     |        |         |         |                  |
| email | Yes      | String  |     |     |        |         |         | Must be a valid email address |

## Person

| Field | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|---------|-----|-----|--------|---------|---------|------------------|
| age   | Yes      | Integer | 0   |     |        |         |         | Must be non-negative |

## UserModel

| Field | Required | Type   | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|--------|-----|-----|--------|---------|---------|------------------|
| email | Yes      | str    |     |     |        |         |         | Must contain "@" |
| age   | Yes      | int    | 0   |     |        |         |         | Must be positive  |

## DynamicUser

No table can be generated for `DynamicUser`.  The code dynamically creates fields, and the validation rules are not consistently applied to all fields.  A static table representation is not possible without knowing all possible field names and their associated validation rules at compile time.

## AdvancedValidationCar

| Field                | Required | Type       | Min      | Max      | Length | Default | Pattern                     | Other Validation             |
|-----------------------|----------|------------|-----------|-----------|--------|---------|-----------------------------|-----------------------------|
| vin                  | Yes      | String     |           |           |        |         |                             |                             |
| ownerName            | Yes      | String     |           |           |        |         |                             | Must not be blank            |
| licensePlate         |          | String     |           |           |        |         | `[A-Z]{2}[0-9]{2} [A-Z]{3}` |                             |
| year                 |          | Integer    | 1886      | 2100      |        |         |                             |                             |
| modelName            |          | String     |           |           | 2-30   |         |                             |                             |
| contactEmail         |          | String     |           |           |        |         |                             | Must be a valid email address |
| numberOfDoors        |          | Integer    | 1         |           |        |         |                             | Must be positive             |
| numberOfPreviousOwners |          | Integer    | 0         |           |        |         |                             | Must be positive or zero     |
| negativeTestValue    |          | Integer    |           |           |        |         |                             | Must be negative             |
| negativeOrZeroTestValue |          | Integer    |           | 0         |        |         |                             | Must be negative or zero     |
| registrationDate     |          | LocalDate  |           |           |        |         |                             | Must be in the past          |
| lastServiceDate      |          | LocalDate  |           |           |        |         |                             | Must be in the past or present |
| insuranceExpiryDate  |          | LocalDate  |           |           |        |         |                             | Must be in the future        |
| warrantyExpiryDate   |          | LocalDate  |           |           |        |         |                             | Must be in the future or present |
| price                |          | BigDecimal | 0.0       | 1000000.0 |        |         |                             |                             |
| engineCapacity       |          | BigDecimal |           |           |        |         |                             | Integer part max 5 digits, 2 decimal places |
| isInsured            |          | Boolean    |           |           |        |         |                             | Must be true                 |
| isStolen             |          | Boolean    |           |           |        |         |                             | Must be false                |

