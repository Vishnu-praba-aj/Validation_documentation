# Validation Documentation: parking_app

## Person

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | Yes |  Integer | 0 |  |  |  |  | Must be a non-negative integer.  |

## UserModel

| Field | Required | Type | Min | Max | Length | Default | Pattern | email_must_have_at | age_positive |
|---|---|---|---|---|---|---|---|---|---|
| email | Yes | str |  |  |  |  |  | must contain @ |  |
| age | Yes | int | 0 |  |  |  |  |  | must be positive |

## DynamicUser

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| age | No |  | 0 |  |  |  |  | Must be positive |
|  | No |  |  |  |  |  |  |  |

## AdvancedValidationCar

| Field             | Required | Type      | Min     | Max      | Length | Default | Pattern                     | Email      | Positive | PositiveOrZero | Negative | NegativeOrZero | Past             | PastOrPresent    | Future            | FutureOrPresent   | DecimalMin     | DecimalMax       | Digits (integer/fraction) | AssertTrue | AssertFalse | Other Validation |
|----------------------|----------|-----------|---------|----------|--------|---------|-----------------------------|-----------|----------|-----------------|----------|-----------------|-----------------|--------------------|--------------------|--------------------|-----------------|-------------------|--------------------------|------------|-------------|-------------------|
| vin                | Yes      | String    |         |          |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| ownerName          | Yes      | String    |         |          |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| licensePlate       | Yes      | String    |         |          |        |         | [A-Z]{2}[0-9]{2} [A-Z]{3} |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| year               | Yes      | int       | 1886    | 2100     |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| modelName          | Yes      | String    |         |          | 2-30   |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| contactEmail       | Yes      | String    |         |          |        |         |                             | Yes       |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| numberOfDoors      | Yes      | int       |         |          |        |         |                             |           | Yes      |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| numberOfPreviousOwners | Yes      | int       |         |          |        |         |                             |           |          | Yes              |          |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| negativeTestValue  | Yes      | int       |         |          |        |         |                             |           |          |                 | Yes      |                 |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| negativeOrZeroTestValue | Yes      | int       |         |          |        |         |                             |           |          |                 |          | Yes              |                 |                    |                    |                    |                 |                 |                          |            |             |                   |
| registrationDate   | Yes      | LocalDate |         |          |        |         |                             |           |          |                 |          |                 | Yes             |                    |                    |                    |                 |                 |                          |            |             |                   |
| lastServiceDate    | Yes      | LocalDate |         |          |        |         |                             |           |          |                 |          |                 |                 | Yes                 |                    |                    |                 |                 |                          |            |             |                   |
| insuranceExpiryDate | Yes      | LocalDate |         |          |        |         |                             |           |          |                 |          |                 |                 |                    | Yes             |                    |                 |                 |                          |            |             |                   |
| warrantyExpiryDate  | Yes      | LocalDate |         |          |        |         |                             |           |          |                 |          |                 |                 |                    |                    | Yes                 |                 |                 |                          |            |             |                   |
| price              | Yes      | BigDecimal| 0.0      | 1000000.0 |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    | Yes             | Yes              |                          |            |             |                   |
| engineCapacity     | Yes      | BigDecimal|         |          |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 | 5/2                     |            |             |                   |
| isInsured          | Yes      | boolean   |         |          |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          | Yes         |             |                   |
| isStolen           | Yes      | boolean   |         |          |        |         |                             |           |          |                 |          |                 |                 |                    |                    |                    |                 |                 |                          |            | Yes          |                   |



## DynamicCar

No validation rules are present in the provided code for the `DynamicCar` class.  The comment indicates that validation would occur dynamically, which is not statically analyzable.

## DynamicObj

| Field           | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-----------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| field_\[random]| No       | Number  |     |     |        | 42      |         |                 |
| name            | Yes      | String  |     |     |        |         |         |                 |

## No validation logic found in provided code.

There is no validation logic present in the provided `app.py` file.  The code sets up a Flask application and registers blueprints, but contains no explicit validation rules for any data fields.  Therefore, no table can be generated.

## User

| Field      | Required | Type      | Min | Max | Length | Default | Pattern        | Other Validation                                      |
|------------|----------|-----------|-----|-----|--------|---------|-----------------|-----------------------------------------------------|
| username   | Yes       | String    |     |     |        |         |                 | Must be unique                                      |
| email      | Yes       | String    |     |     |        |         |                 | Must be unique, must be a valid email address (HTML5) |
| password   | Yes       | String    |     |     |        |         |                 |                                                     |

## ParkingLot

| Field                | Required | Type             | Min | Max | Length | Default | Pattern | Other Validation |
|-----------------------|----------|-------------------|-----|-----|--------|---------|---------|-----------------|
| prime_location_name  | Yes      | String           |     |     |        |         |         |                 |
| price_per_hour       | Yes      | Float            |     |     |        |         |         |                 |
| address              | Yes      | String           |     |     |        |         |         |                 |
| pin_code             | Yes      | String           |     |     |        |         |         |                 |
| max_number_of_spots | Yes      | Integer          |     |     |        |         |         |                 |



## ParkingSpot

| Field         | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-----------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| lot_id        | Yes      | Integer |     |     |        |         |         |                 |
| spot_number    | Yes      | String  |     |     |        |         |         |                 |
| status         | Yes      | String  |     |     |        | 'A'     |         |                 |



## Reservation

| Field               | Required | Type             | Min | Max | Length | Default | Pattern | Other Validation |
|-----------------------|----------|-------------------|-----|-----|--------|---------|---------|-----------------|
| spot_id              | Yes      | Integer          |     |     |        |         |         |                 |
| user_id              | Yes      | Integer          |     |     |        |         |         |                 |
| parking_timestamp    | Yes      | DateTime         |     |     |        |         |         |                 |
| leaving_timestamp    | No       | DateTime         |     |     |        |         |         |                 |
| parking_cost         | No       | Float            |     |     |        |         |         |                 |



## Book Parking Request (from request.json)

| Field     | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| user_id    | Yes      | Integer |     |     |        |         |         |                 |



## Update Parking Lot Request (from request.json)

| Field                | Required | Type             | Min | Max | Length | Default | Pattern | Other Validation |
|-----------------------|----------|-------------------|-----|-----|--------|---------|---------|-----------------|
| prime_location_name  | No       | String           |     |     |        |         |         |                 |
| price_per_hour       | No       | Float            |     |     |        |         |         |                 |
| address              | No       | String           |     |     |        |         |         |                 |
| pin_code             | No       | String           |     |     |        |         |         |                 |
| max_number_of_spots | No       | Integer          |     |     |        |         |         |                 |

## parking_lot

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | INTEGER |  |  |  |  |  |  |
| prime_location_name | Yes | VARCHAR |  |  | 100 |  |  |  |
| price_per_hour | Yes | FLOAT |  |  |  |  |  |  |
| address | Yes | VARCHAR |  |  | 200 |  |  |  |
| pin_code | Yes | VARCHAR |  |  | 10 |  |  |  |
| max_number_of_spots | Yes | INTEGER |  |  |  |  |  |  |



## parking_spot

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | INTEGER |  |  |  |  |  |  |
| lot_id | Yes | INTEGER |  |  |  |  |  |  |
| spot_number | Yes | VARCHAR |  |  | 10 |  |  |  |
| status | Yes | VARCHAR |  |  | 1 |  |  |  |



## reservation

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | INTEGER |  |  |  |  |  |  |
| spot_id | Yes | INTEGER |  |  |  |  |  |  |
| user_id | Yes | INTEGER |  |  |  |  |  |  |
| parking_timestamp |  | DATETIME |  |  |  |  |  |  |
| leaving_timestamp |  | DATETIME |  |  |  |  |  |  |
| parking_cost |  | FLOAT |  |  |  |  |  |  |



## admin

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | INTEGER |  |  |  |  |  |  |
| username |  | VARCHAR |  |  | 50 |  |  |  |
| password |  | VARCHAR |  |  | 100 |  |  |  |



## user

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | INTEGER |  |  |  |  |  |  |
| username |  | VARCHAR |  |  | 80 |  |  |  |
| email |  | VARCHAR |  |  | 120 |  |  |  |
| password |  | VARCHAR |  |  | 200 |  |  |  |

## Admin

| Field      | Required | Type      | Min | Max | Length | Default | Pattern | Other Validation |
|------------|----------|-----------|-----|-----|--------|---------|---------|-----------------|
| id         | No       | Integer   |     |     |        |         |         | Unique (primary key) |
| username   | Yes      | String    |     |     | 50     |         |         | Unique           |
| password   | Yes      | String    |     |     | 100    |         |         |                  |

## Car

| Field          | Required | Type    | Min     | Max | Length | Default | Pattern | Other Validation           |
|-----------------|----------|---------|---------|-----|--------|---------|---------|-------------------------------|
| licensePlate    | Yes      | String  |         |     | 5      |         |         |                               |
| year            | Yes      | int     | 1886    |     |        |         |         |                               |



## Product

| Field      | Required | Type   | Min | Max | Length | Default | Pattern | Other Validation              |
|-------------|----------|--------|-----|-----|--------|---------|---------|---------------------------------|
| name       | Yes      | String |     |     |        |         |         |                                 |
| price      | Yes      | number | 0   |     |        |         |         | Must be non-negative            |



## Inventory

| Field      | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|--------|---------|---------|--------------------|
| items      | No       | Array   |     |     |        |         |         |                   |

