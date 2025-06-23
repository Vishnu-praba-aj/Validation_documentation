# Validation Documentation: parking_app

## Person

| Field | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| age   | Yes      | Integer | 0   |     |        |         |         | `validate_age` function |

## UserModel

| Field | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------|-----------|---------|-----|-----|--------|---------|---------|-----------------|
| email | Yes       | String  |     |     |        |         |         | must contain @   |
| age   | Yes       | Integer | 0   |     |        |         |         | must be positive |

## DynamicUser

| Field | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| age   | No       | Integer | 0   |     |        |         |         | Age must be positive |
| other fields | No | Any | | | | | | |

## AdvancedValidationCar

| Field             | Required | Type     | Min     | Max      | Length | Default | Pattern                      | Email      | Positive | PositiveOrZero | Negative | NegativeOrZero | Past             | PastOrPresent    | Future            | FutureOrPresent   | DecimalMin     | DecimalMax       | Digits            | AssertTrue | AssertFalse | Other Validation |
|----------------------|----------|----------|----------|----------|---------|---------|------------------------------|------------|----------|-----------------|----------|-----------------|-----------------|--------------------|--------------------|--------------------|-----------------|-------------------|--------------------|-------------|-------------|-------------------|
| vin                | Yes      | String   |          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| ownerName          | Yes      | String   |          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| licensePlate       | Yes      | String   |          |          |         |         | [A-Z]{2}[0-9]{2} [A-Z]{3} |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| year               | Yes      | Integer  | 1886     | 2100     |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| modelName          | Yes      | String   |          |          | 2-30    |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| contactEmail       | Yes      | String   |          |          |         |         |                              | Yes        |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| numberOfDoors      | Yes      | Integer  |          |          |         |         |                              |            | Yes      |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| numberOfPreviousOwners | Yes      | Integer  |          |          |         |         |                              |            |          | Yes              |          |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| negativeTestValue  | Yes      | Integer  |          |          |         |         |                              |            |          |                  | Yes      |                  |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| negativeOrZeroTestValue | Yes      | Integer  |          |          |         |         |                              |            |          |                  |          | Yes              |                 |                    |                    |                    |                 |                  |                    |             |             |                   |
| registrationDate   | Yes      | LocalDate |          |          |         |         |                              |            |          |                  |          |                  | Yes             |                    |                    |                    |                 |                  |                    |             |             |                   |
| lastServiceDate    | Yes      | LocalDate |          |          |         |         |                              |            |          |                  |          |                  |                 | Yes                 |                    |                    |                 |                  |                    |             |             |                   |
| insuranceExpiryDate| Yes      | LocalDate |          |          |         |         |                              |            |          |                  |          |                  |                 |                    | Yes             |                    |                 |                  |                    |             |             |                   |
| warrantyExpiryDate | Yes      | LocalDate |          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    | Yes                 |                 |                  |                    |             |             |                   |
| price              | Yes      | BigDecimal|          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    | 0.0              | 1000000.0         |                    |             |             |                   |
| engineCapacity     | Yes      | BigDecimal|          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  | 5,2               |             |             |                   |
| isInsured          | Yes      | Boolean   |          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    | Yes           |             |                   |
| isStolen           | Yes      | Boolean   |          |          |         |         |                              |            |          |                  |          |                  |                 |                    |                    |                    |                 |                  |                    |             | Yes           |                   |



## DynamicCar

No validation rules are present in this class.  It uses dynamic field setting, which is not statically analyzable for validation purposes.

## DynamicObj

| Field             | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|----------------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| field_X (dynamic) | No       | Number  |     |     |        | 42      |         |                  |

## User

| Field      | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation                                      |
|------------|----------|---------|-----|-----|--------|---------|---------|------------------------------------------------------|
| username   | Yes      | String  |     |     |        |         |         | Must be unique                                      |
| email      | Yes      | String  |     |     |        |         |         | Must be unique, valid email format (implicitly via HTML type="email") |
| password   | Yes      | String  |     |     |        |         |         |                                                      |

## ParkingLot

| Field                | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|----------------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| prime_location_name | Yes      | String  |     |     |        |         |         |                 |
| price_per_hour      | Yes      | Float   |     |     |        |         |         |                 |
| address              | Yes      | String  |     |     |        |         |         |                 |
| pin_code            | Yes      | String  |     |     |        |         |         |                 |
| max_number_of_spots | Yes      | Integer |     |     |        |         |         |                 |



## ParkingSpot

| Field       | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| lot_id      | Yes      | Integer |     |     |        |         |         |                 |
| spot_number | Yes      | String  |     |     |        |         |         |                 |
| status      | Yes      | String  |     |     |        | A       |         |                 |



## Reservation

| Field             | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|--------------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| spot_id           | Yes      | Integer |     |     |        |         |         |                 |
| user_id           | Yes      | Integer |     |     |        |         |         |                 |
| parking_timestamp | Yes      | DateTime|     |     |        |         |         |                 |
| leaving_timestamp | No       | DateTime|     |     |        |         |         |                 |
| parking_cost      | No       | Float   |     |     |        |         |         |                 |



## Book Parking Spot Request (JSON)

| Field     | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| user_id    | Yes      | Integer |     |     |        |         |         |                 |



## Update Parking Lot Request (JSON)

| Field                | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|----------------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| prime_location_name | No       | String  |     |     |        |         |         |                 |
| price_per_hour      | No       | Float   |     |     |        |         |         |                 |
| address              | No       | String  |     |     |        |         |         |                 |
| pin_code            | No       | String  |     |     |        |         |         |                 |
| max_number_of_spots | No       | Integer |     |     |        |         |         |                 |

## parking_lot

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | Integer |  |  |  |  |  |  |
| prime_location_name | Yes | String |  |  | 100 |  |  |  |
| price_per_hour | Yes | Float |  |  |  |  |  |  |
| address | Yes | String |  |  | 200 |  |  |  |
| pin_code | Yes | String |  |  | 10 |  |  |  |
| max_number_of_spots | Yes | Integer |  |  |  |  |  |  |



## parking_spot

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | Integer |  |  |  |  |  |  |
| lot_id | Yes | Integer |  |  |  |  |  |  |
| spot_number | Yes | String |  |  | 10 |  |  |  |
| status | Yes | String |  |  | 1 |  |  |  |



## reservation

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | Integer |  |  |  |  |  |  |
| spot_id | Yes | Integer |  |  |  |  |  |  |
| user_id | Yes | Integer |  |  |  |  |  |  |
| parking_timestamp |  | DateTime |  |  |  |  |  |  |
| leaving_timestamp |  | DateTime |  |  |  |  |  |  |
| parking_cost |  | Float |  |  |  |  |  |  |



## admin

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | Integer |  |  |  |  |  |  |
| username |  | String |  |  | 50 |  |  |  |
| password |  | String |  |  | 100 |  |  |  |



## user

| Field | Required | Type | Min | Max | Length | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|---|
| id | Yes | Integer |  |  |  |  |  |  |
| username |  | String |  |  | 80 |  |  |  |
| email |  | String |  |  | 120 |  |  |  |
| password |  | String |  |  | 200 |  |  |  |

## Admin

| Field      | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|--------|---------|---------|-----------------|
| id          | Yes      | Integer |     |     |        |         |         | Unique (primary key) |
| username    | Yes      | String  |     |     | 50     |         |         | Unique           |
| password    | Yes      | String  |     |     | 100    |         |         |                  |

## Car

| Field          | Required | Type    | Min      | Max | Length | Default | Pattern | Other Validation |
|-----------------|----------|---------|----------|-----|--------|---------|---------|-------------------|
| licensePlate    | Yes      | String  |          |     | 5       |         |         |                  |
| year            | Yes      | Integer | 1886     |     |        |         |         |                  |



## Product

| Field      | Required | Type    | Min | Max | Length | Default | Pattern | Other Validation          |
|------------|----------|---------|-----|-----|--------|---------|---------|--------------------------|
| name       | Yes      | String  |     |     |        |         |         |                          |
| price      | Yes      | Number  | 0    |     |        |         |         | Must be non-negative     |



## Inventory

| Field | Required | Type       | Min | Max | Length | Default | Pattern | Other Validation |
|-------|----------|------------|-----|-----|--------|---------|---------|-------------------|
| items | No       | Array      |     |     |        |         |         |                  |

##  No validation logic found in provided code.

There is no explicit validation logic present in the provided `templates/app.py` file.  The code sets up a Flask application, initializes a database, and registers blueprints, but doesn't contain any validation rules for data fields.  To create validation tables, the code for models (`models.py`) and controllers (`controllers/auth.py`, `controllers/parking_controller.py`) needs to be provided.

