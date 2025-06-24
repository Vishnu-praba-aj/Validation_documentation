# Validation Documentation: sample.git

## CrossFileUtils

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age |  No  | Integer | 0 |  |  |  |  | Must not be negative |

## User

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| name | Yes | String |  |  |  |  |  |  |
| age | Yes | Integer | 0 |  |  |  |  | Must be non-negative |

## UserController

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| name | Yes | String |  |  |  |  |  |  |
| age | Yes | Integer | 18 |  |  |  |  |  |
| email | Yes | String |  |  |  |  | email |  |

## Person

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  |  | Must not be negative |

## UserModel

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| email | Yes | String |  |  |  |  |  | Must contain "@" |
| age | Yes | Integer | 0 |  |  |  |  | Must be positive |

## DynamicUser

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | No | Integer | 0 |  |  |  |  | Must be positive |

## AdvancedValidationCar

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| vin | Yes | String |  |  |  |  |  |  |
| ownerName | Yes | String |  |  |  |  |  | Must not be blank |
| licensePlate |  | String |  |  |  |  | [A-Z]{2}[0-9]{2} [A-Z]{3} |  |
| year |  | Integer | 1886 | 2100 |  |  |  |  |
| modelName |  | String |  |  | 2 | 30 |  |  |
| contactEmail |  | String |  |  |  |  | email |  |
| numberOfDoors |  | Integer | 0 |  |  |  |  | Must be positive |
| numberOfPreviousOwners |  | Integer | 0 |  |  |  |  | Must be positive or zero |
| negativeTestValue |  | Integer |  |  |  |  |  | Must be negative |
| negativeOrZeroTestValue |  | Integer |  |  |  |  |  | Must be negative or zero |
| registrationDate |  | LocalDate |  |  |  |  |  | Must be in the past |
| lastServiceDate |  | LocalDate |  |  |  |  |  | Must be in the past or present |
| insuranceExpiryDate |  | LocalDate |  |  |  |  |  | Must be in the future |
| warrantyExpiryDate |  | LocalDate |  |  |  |  |  | Must be in the future or present |
| price |  | BigDecimal | 0.0 | 1000000.0 |  |  |  |  |
| engineCapacity |  | BigDecimal |  |  |  |  |  | Digits(integer=5, fraction=2) |
| isInsured |  | Boolean |  |  |  |  |  | Must be true |
| isStolen |  | Boolean |  |  |  |  |  | Must be false |

