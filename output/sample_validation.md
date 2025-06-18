# Validation Documentation: sample

## User

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name |  | String |  |  |  |  |  |
| age |  | int | 0 |  |  |  | Must be non-negative |

## Person

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be non-negative |



## CrossFileUtils (Inferred from usage)

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  |  |

## UserModel

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| email | True | str |  |  |  |  | must contain @ |
| age | True | int | 0 |  |  |  |  |

## DynamicUser

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age |  |  | 0 |  |  |  | Must be positive |

## AdvancedValidationCar

| Field             | Required | Type       | Min     | Max      | Pattern                     | Email     | Positive | PositiveOrZero | Negative | NegativeOrZero | Past          | PastOrPresent | Future         | FutureOrPresent | DecimalMin    | DecimalMax      | Digits (integer,fraction) | AssertTrue | AssertFalse | Size (min, max) | Other Validation |
|----------------------|----------|------------|---------|----------|-----------------------------|-----------|----------|-----------------|----------|-----------------|---------------|---------------|----------------|-----------------|----------------|-----------------|-----------------------|-------------|-------------|-----------------|--------------------|
| vin                 | Yes      | String     |          |          |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| ownerName           | Yes      | String     |          |          |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| licensePlate        |          | String     |          |          | [A-Z]{2}[0-9]{2} [A-Z]{3} |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| year                |          | int        | 1886    | 2100     |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| modelName           |          | String     |          |          |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             | 2, 30            |                    |
| contactEmail        |          | String     |          |          |                             | Yes       |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| numberOfDoors       |          | int        |          |          |                             |           | Yes      |                 |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| numberOfPreviousOwners |          | int        |          |          |                             |           |          | Yes              |          |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| negativeTestValue    |          | int        |          |          |                             |           |          |                 | Yes      |                 |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| negativeOrZeroTestValue |          | int        |          |          |                             |           |          |                 |          | Yes              |               |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| registrationDate    |          | LocalDate  |          |          |                             |           |          |                 |          |                 | Yes           |               |                 |                 |                 |                 |                       |             |             |                 |                    |
| lastServiceDate     |          | LocalDate  |          |          |                             |           |          |                 |          |                 |               | Yes           |                 |                 |                 |                 |                       |             |             |                 |                    |
| insuranceExpiryDate |          | LocalDate  |          |          |                             |           |          |                 |          |                 |               |               | Yes           |                 |                 |                 |                       |             |             |                 |                    |
| warrantyExpiryDate  |          | LocalDate  |          |          |                             |           |          |                 |          |                 |               |               |                 | Yes              |                 |                 |                       |             |             |                 |                    |
| price               |          | BigDecimal |          |          |                             |           |          |                 |          |                 |               |               |                 |                 | 0.0             | 1000000.0        |                       |             |             |                 |                    |
| engineCapacity      |          | BigDecimal |          |          |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 | 5, 2                 |             |             |                 |                    |
| isInsured           |          | boolean    |          |          |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       | Yes          |             |                 |                    |
| isStolen            |          | boolean    |          |          |                             |           |          |                 |          |                 |               |               |                 |                 |                 |                 |                       |             | Yes          |                 |                    |

