# Validation Documentation: parking_app

## Person

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be non-negative |

## `validate_age` Function

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be non-negative (raises ValueError if < 0) |


There's only one validation function provided, `validate_age`,  so only one table is needed.  No other validation logic was present in the provided source code or dependencies.

## UserModel

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation | email_must_have_at | age_positive |
|---|---|---|---|---|---|---|---|---|---|
| email | True | str |  |  |  |  | must contain @ | ✅ |  |
| age | True | int | 0 |  |  |  | must be positive |  | ✅ |

## DynamicUser

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|---------|---------|-----------------|
| age        |          | Integer | 0   |     |         |         | Must be positive |
| `field_name` | Yes | String |  |  | | |  |
| `value` | Yes |  Any |  |  | | |  |



## Dependency `__init__` (Implicit in `validate_age`)

The provided dependency snippet doesn't specify the exact validation logic within `validate_age`.  Therefore, a more complete definition of `validate_age` is needed to populate the table below.  Assumptions are made below in the absence of its definition.


| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|---------|---------|-----------------|
| age        | Yes      | Integer | 0   |     |         |         |  (Assuming `validate_age` enforces positivity) |


**Note:** The validation rules are inferred from the provided code snippets.  A more comprehensive understanding of `validate_age` is crucial for a complete and accurate validation summary.  The `value` field in `DynamicUser` has no explicit validation beyond whatever type checking `setattr` might inherently perform.  Similarly,  `field_name` in `DynamicUser` has no explicit validation.  The "Yes" in the "Required" columns reflects that the constructors require these values to be supplied.

## AdvancedValidationCar

| Field             | Required | Type        | Min      | Max      | Default | Pattern                     | Email     | Positive | PositiveOrZero | Negative | NegativeOrZero | Past             | PastOrPresent   | Future            | FutureOrPresent | DecimalMin | DecimalMax     | Digits (integer,fraction) | AssertTrue | AssertFalse | Size (min, max) | Other Validation |
|----------------------|----------|-------------|-----------|-----------|---------|-----------------------------|-----------|----------|-----------------|----------|-----------------|-----------------|-----------------|-----------------|-----------------|-------------|-----------------|------------------------|------------|-------------|-----------------|-----------------|
| vin                | Yes       | String      |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| ownerName          | Yes       | String      |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| licensePlate       | Yes       | String      |           |           |         | `[A-Z]{2}[0-9]{2} [A-Z]{3}` |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| year               | Yes       | int         | 1886      | 2100      |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| modelName          | Yes       | String      |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             | 2, 30           |                 |
| contactEmail       | Yes       | String      |           |           |         |                             | Yes       |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| numberOfDoors      | Yes       | int         |           |           |         |                             |           | Yes      |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| numberOfPreviousOwners | Yes       | int         |           |           |         |                             |           |          | Yes              |          |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| negativeTestValue  | Yes       | int         |           |           |         |                             |           |          |                 | Yes      |                 |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| negativeOrZeroTestValue | Yes       | int         |           |           |         |                             |           |          |                 |          | Yes              |                 |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| registrationDate   | Yes       | LocalDate   |           |           |         |                             |           |          |                 |          |                 | Yes              |                 |                 |                 |             |                 |                        |            |             |                 |                 |
| lastServiceDate    | Yes       | LocalDate   |           |           |         |                             |           |          |                 |          |                 |                 | Yes              |                 |                 |             |                 |                        |            |             |                 |                 |
| insuranceExpiryDate | Yes       | LocalDate   |           |           |         |                             |           |          |                 |          |                 |                 |                 | Yes              |                 |             |                 |                        |            |             |                 |                 |
| warrantyExpiryDate  | Yes       | LocalDate   |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 | Yes              |             |                 |                        |            |             |                 |                 |
| price              | Yes       | BigDecimal  | 0.0        | 1000000.0 |         |                             |           |          |                 |          |                 |                 |                 |                 |                 | Yes          | Yes             |                        |            |             |                 |                 |
| engineCapacity     | Yes       | BigDecimal  |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 | 5, 2                |            |             |                 |                 |
| isInsured          | Yes       | boolean     |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        | Yes         |             |                 |                 |
| isStolen           | Yes       | boolean     |           |           |         |                             |           |          |                 |          |                 |                 |                 |                 |                 |             |                 |                        |            | Yes          |                 |                 |



## DynamicCar

No validation logic is present in this class.  The comment indicates that validation would happen dynamically at runtime, which is outside the scope of static code analysis.

## DynamicObj

| Field           | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|-----------------|----------|---------|-----|-----|---------|---------|-------------------|
| `field_*`       |          | Number  |     |     | 42      |         | Dynamically named; generated randomly during object creation |
|  `name` (set via `setField`) |          |  Any    |     |     |         |         | No explicit validation in `setField` itself.  Validation depends on how `setField` is used. |


**Note:** The `DynamicObj` class has dynamically generated field names, making static validation difficult.  The table reflects the known aspects of the validation:  a number field is created with a default of 42.  However, subsequent calls to `setField` could add fields of any type and with any constraints not explicitly encoded in the provided code.  Therefore, validation heavily depends on external factors and the context of how `setField` is utilized.

## User

| Field      | Required | Type    | Min | Max | Default | Pattern             | Other Validation                                      |
|-------------|----------|---------|-----|-----|---------|----------------------|------------------------------------------------------|
| username   | Yes      | String  |     |     |         |                      | Must be unique                                      |
| email      | Yes      | String  |     |     |         |                      | Must be unique, valid email format (HTML5 type="email") |
| password   | Yes      | String  |     |     |         |                      |                                                      |



## Login

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation                     |
|-------------|----------|---------|-----|-----|---------|---------|--------------------------------------|
| username   | Yes      | String  |     |     |         |         |                                      |
| password   | Yes      | String  |     |     |         |         | Must match stored password in database |

## ParkingLot

| Field                | Required | Type             | Min     | Max     | Default | Pattern | Other Validation                                                                    |
|-----------------------|----------|-----------------|---------|---------|---------|---------|------------------------------------------------------------------------------------|
| prime_location_name | Yes      | String          |         |         |         |         |                                                                                    |
| price_per_hour       | Yes      | Float/Decimal   |         |         |         |         | Must be a non-negative number                                                    |
| address              | Yes      | String          |         |         |         |         |                                                                                    |
| pin_code             | Yes      | String          |         |         |         |         |                                                                                    |
| max_number_of_spots  | Yes      | Integer         | 1       |         |         |         | Must be greater than or equal to the number of currently occupied spots on delete |



## ParkingSpot

| Field          | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|-----------------|----------|---------|-----|-----|---------|---------|-------------------|
| lot_id         | Yes      | Integer |     |     |         |         |                  |
| spot_number    | Yes      | String  |     |     |         |         |                  |
| status         | Yes      | String  |     |     | 'A'    |         | 'A' for Available, 'O' for Occupied |



## Reservation

| Field                | Required | Type             | Min     | Max     | Default | Pattern | Other Validation                                               |
|-----------------------|----------|-----------------|---------|---------|---------|---------|-------------------------------------------------------------------|
| spot_id              | Yes      | Integer         |         |         |         |         |                                                                   |
| user_id              | Yes      | Integer         |         |         |         |         |                                                                   |
| parking_timestamp    | Yes      | DateTime        |         |         |         |         | Automatically set to current UTC time upon creation             |
| leaving_timestamp    | No       | DateTime        |         |         |         |         | Set upon release of the spot; null initially                    |
| parking_cost         | No       | Float/Decimal   | 0       |         | 0       |         | Calculated upon spot release based on duration and price per hour |




## Book Parking Spot Request

| Field    | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|----------|----------|---------|-----|-----|---------|---------|-------------------|
| user_id  | Yes      | Integer |     |     |         |         |                  |



## Update Parking Lot Request

| Field                | Required | Type             | Min     | Max     | Default | Pattern | Other Validation                                                              |
|-----------------------|----------|-----------------|---------|---------|---------|---------|---------------------------------------------------------------------------------|
| max_number_of_spots  | No       | Integer         |         |         |         |         | Must be greater than or equal to the number of currently occupied spots     |
| prime_location_name | No       | String          |         |         |         |         |                                                                                |
| price_per_hour       | No       | Float/Decimal   |         |         |         |         | Must be a non-negative number                                                |
| address              | No       | String          |         |         |         |         |                                                                                |
| pin_code             | No       | String          |         |         |         |         |                                                                                |

## Admin

| Field      | Required | Type      | Min | Max | Default | Pattern | Other Validation |
|--------------|----------|-----------|-----|-----|---------|---------|-------------------|
| username    | True     | String    |     | 50  |         |         | Unique             |
| password    |          | String    |     | 100 |         |         |                   |

## Car (Java)

| Field          | Required | Type    | Min     | Max     | Default | Pattern | Other Validation                     |
|-----------------|----------|---------|---------|---------|---------|---------|--------------------------------------|
| licensePlate   | Yes      | String  | 5       |         |         |         | Minimum length of 5 characters        |
| year           | Yes      | Integer | 1886    |         |         |         | Must be greater than or equal to 1886 |



## Product (JavaScript)

| Field | Required | Type   | Min | Max | Default | Pattern | Other Validation                |
|-------|----------|--------|-----|-----|---------|---------|------------------------------------|
| name  | Yes      | String |     |     |         |         |                                    |
| price | Yes      | Number | 0   |     |         |         | Must be non-negative             |



## Inventory (JavaScript)

| Field | Required | Type    | Min | Max | Default | Pattern | Other Validation          |
|-------|----------|---------|-----|-----|---------|---------|-----------------------------|
| item  | Yes      | Object  |     |     |         |         | Must have a name property |

