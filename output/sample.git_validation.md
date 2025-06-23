# Validation Documentation: sample.git

## CrossFileUtils

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | Yes | int | 0 |  |  |  |  | Must not be negative |

## User

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| name | No | String |  |  |  |  |  |  |
| age | Yes | int | 0 |  |  |  |  | Age must be non-negative |

## Person

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | Yes | int | 0 |  |  |  |  | Must be non-negative |



## UserModel

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| email | Yes | str |  |  |  |  |  | must contain @ |
| age | Yes | int | 0 |  |  |  |  | must be positive |

## DynamicUser

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | No |  | 0 |  |  |  |  | Must be positive |
|  | No |  |  |  |  |  |  |  |

## AdvancedValidationCar

| Field             | Required | Type      | Min     | Max      | Length | Default | Pattern                     | Email     | Positive | PositiveOrZero | Negative | NegativeOrZero | Past                | PastOrPresent      | Future               | FutureOrPresent     | DecimalMin | DecimalMax      | Digits (integer,fraction) | AssertTrue | AssertFalse | Other Validation |
|----------------------|----------|-----------|----------|----------|---------|---------|-----------------------------|-----------|----------|-----------------|----------|-----------------|----------------------|----------------------|----------------------|----------------------|-------------|-----------------|--------------------------|-------------|-------------|-------------------|
| vin                 | Yes      | String    |          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| ownerName           | Yes      | String    |          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| licensePlate        | Yes      | String    |          |          |         |         | [A-Z]{2}[0-9]{2} [A-Z]{3} |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| year                | Yes      | int       | 1886     | 2100     |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| modelName           | Yes      | String    |          |          | 2-30    |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| contactEmail        | Yes      | String    |          |          |         |         |                             | Yes       |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| numberOfDoors       | Yes      | int       |          |          |         |         |                             |           | Yes      |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| numberOfPreviousOwners | Yes      | int       |          |          |         |         |                             |           |          | Yes              |          |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| negativeTestValue   | Yes      | int       |          |          |         |         |                             |           |          |                 | Yes      |                 |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| negativeOrZeroTestValue | Yes      | int       |          |          |         |         |                             |           |          |                 |          | Yes              |                      |                      |                      |                      |             |                 |                          |             |             |                   |
| registrationDate    | Yes      | LocalDate |          |          |         |         |                             |           |          |                 |          |                 | Yes                 |                      |                      |                      |             |                 |                          |             |             |                   |
| lastServiceDate     | Yes      | LocalDate |          |          |         |         |                             |           |          |                 |          |                 |                      | Yes                 |                      |                      |             |                 |                          |             |             |                   |
| insuranceExpiryDate | Yes      | LocalDate |          |          |         |         |                             |           |          |                 |          |                 |                      |                      | Yes                 |                      |             |                 |                          |             |             |                   |
| warrantyExpiryDate  | Yes      | LocalDate |          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      | Yes                 |             |                 |                          |             |             |                   |
| price               | Yes      | BigDecimal|          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      | 0.0         | 1000000.0        |                          |             |             |                   |
| engineCapacity      | Yes      | BigDecimal|          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 | 5,2                     |             |             |                   |
| isInsured           | Yes      | boolean   |          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          | Yes         |             |                   |
| isStolen            | Yes      | boolean   |          |          |         |         |                             |           |          |                 |          |                 |                      |                      |                      |                      |             |                 |                          |             | Yes         |                   |

