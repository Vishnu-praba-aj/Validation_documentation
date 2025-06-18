# Validation Documentation: parking_app

## Person

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be a non-negative integer.  |

## UserModel

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| email | True | str |  |  |  |  | must contain @ |
| age | True | int | 0 |  |  |  | must be positive |

## DynamicUser

| Field | Required | Type | Min | Max | Default | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age |  |  | 0 |  |  |  | Must be positive |

## AdvancedValidationCar

| Field             | Required | Type        | Min     | Max      | Default | Pattern                  | Email    | Positive | PositiveOrZero | Negative | NegativeOrZero | Past             | PastOrPresent      | Future            | FutureOrPresent    | DecimalMin      | DecimalMax        | Digits (integer,fraction) | AssertTrue | AssertFalse | Size (min, max) | Other Validation |
|----------------------|----------|-------------|---------|----------|---------|--------------------------|----------|----------|-----------------|----------|-----------------|-----------------|--------------------|-----------------|--------------------|-----------------|--------------------|------------------------|-------------|-------------|-----------------|-------------------|
| vin                 | Yes      | String      |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| ownerName           | Yes      | String      |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| licensePlate        |          | String      |         |          |         | [A-Z]{2}[0-9]{2} [A-Z]{3} |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| year                |          | int         | 1886    | 2100     |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| modelName           |          | String      |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             | 2, 30             |                   |
| contactEmail        |          | String      |         |          |         |                          | Yes      |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| numberOfDoors       |          | int         |         |          |         |                          |          | Yes      |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| numberOfPreviousOwners|          | int         |         |          |         |                          |          |          | Yes              |          |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| negativeTestValue   |          | int         |         |          |         |                          |          |          |                 | Yes      |                 |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| negativeOrZeroTestValue |          | int         |         |          |         |                          |          |          |                 |          | Yes              |                 |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| registrationDate    |          | LocalDate   |         |          |         |                          |          |          |                 |          |                 | Yes             |                    |                 |                    |                 |                 |                        |             |             |                 |                   |
| lastServiceDate     |          | LocalDate   |         |          |         |                          |          |          |                 |          |                 |                 | Yes                 |                 |                    |                 |                 |                        |             |             |                 |                   |
| insuranceExpiryDate |          | LocalDate   |         |          |         |                          |          |          |                 |          |                 |                 |                    | Yes             |                    |                 |                 |                        |             |             |                 |                   |
| warrantyExpiryDate  |          | LocalDate   |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 | Yes                 |                 |                 |                        |             |             |                 |                   |
| price               |          | BigDecimal  | 0.0      | 1000000.0 |         |                          |          |          |                 |          |                 |                 |                    |                 |                    | 0.0              | 1000000.0        |                        |             |             |                 |                   |
| engineCapacity      |          | BigDecimal  |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 | 5, 2                   |             |             |                 |                   |
| isInsured           |          | boolean     |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        | Yes           |             |                 |                   |
| isStolen            |          | boolean     |         |          |         |                          |          |          |                 |          |                 |                 |                    |                 |                    |                 |                 |                        |             | Yes           |                 |                   |



## DynamicCar

No validation logic is present within the provided `DynamicCar` class.  The comment indicates that validation would occur dynamically (likely using reflection), which is outside the scope of static analysis.

## DynamicObj

| Field           | Required | Type   | Min | Max | Default | Pattern | Other Validation |
|-----------------|----------|--------|-----|-----|---------|---------|-------------------|
| `field_XXX`     |          |        |     |     |         |         |  Dynamically assigned at construction; name is random. |
| other fields   |          |        |     |     |         |         | Set dynamically via `setField`; no inherent validation. |

##  No Validation Logic Found

No explicit validation logic was found within the provided `app.py` file.  The code primarily focuses on application setup and routing.  Validation rules might exist within the `models.py` (database models) or within the controllers (`auth.py`, `parking_controller.py`) which were not provided.

## User

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation                                      |
|------------|----------|---------|-----|-----|---------|---------|------------------------------------------------------|
| username   | Yes      | String  |     |     |         |         | Must be unique                                      |
| email      | Yes      | String  |     |     |         |         | Must be unique, must be a valid email format (implicit from HTML type="email") |
| password   | Yes      | String  |     |     |         |         |                                                      |

## ParkingLot

| Field                | Required | Type             | Min     | Max     | Default | Pattern | Other Validation                                      |
|-----------------------|----------|-----------------|---------|---------|---------|---------|------------------------------------------------------|
| prime_location_name | Yes      | String           |         |         |         |         |                                                      |
| price_per_hour       | Yes      | Float            |         |         |         |         | Must be a positive number                             |
| address              | Yes      | String           |         |         |         |         |                                                      |
| pin_code             | Yes      | String           |         |         |         |         |                                                      |
| max_number_of_spots  | Yes      | Integer          | 1       |         |         |         | Must be a positive integer; check for occupied spots on delete |



## ParkingSpot

| Field        | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|--------------|----------|---------|-----|-----|---------|---------|--------------------|
| lot_id       | Yes      | Integer |     |     |         |         |                    |
| spot_number  | Yes      | String  |     |     |         |         |                    |
| status       | Yes      | String  |     |     | 'A'     |         | Must be 'A' or 'O' |



## Reservation

| Field              | Required | Type             | Min   | Max   | Default | Pattern | Other Validation                               |
|----------------------|----------|-----------------|-------|-------|---------|---------|---------------------------------------------------|
| spot_id             | Yes      | Integer          |       |       |         |         |                                                   |
| user_id             | Yes      | Integer          |       |       |         |         |                                                   |
| parking_timestamp   | Yes      | DateTime         |       |       |         |         | Automatically set to current UTC time on creation |
| leaving_timestamp   | No       | DateTime         |       |       |         |         | Automatically set to current UTC time on release  |
| parking_cost        | No       | Float            |       |       | 0       |         | Calculated based on duration and price per hour     |



## parking_lot

| Field                | Required | Type        | Min | Max | Default | Pattern | Other Validation |
|------------------------|----------|-------------|-----|-----|---------|---------|-----------------|
| id                    | ✓        | INTEGER     |     |     |         |         |                 |
| prime_location_name   | ✓        | VARCHAR(100)|     |     |         |         |                 |
| price_per_hour        | ✓        | FLOAT       |     |     |         |         |                 |
| address               | ✓        | VARCHAR(200)|     |     |         |         |                 |
| pin_code              | ✓        | VARCHAR(10) |     |     |         |         |                 |
| max_number_of_spots   | ✓        | INTEGER     |     |     |         |         |                 |



## parking_spot

| Field          | Required | Type        | Min | Max | Default | Pattern | Other Validation |
|-----------------|----------|-------------|-----|-----|---------|---------|-----------------|
| id              | ✓        | INTEGER     |     |     |         |         |                 |
| lot_id          | ✓        | INTEGER     |     |     |         |         |                 |
| spot_number     | ✓        | VARCHAR(10) |     |     |         |         |                 |
| status          | ✓        | VARCHAR(1)  |     |     |         |         |                 |



## reservation

| Field                | Required | Type        | Min | Max | Default | Pattern | Other Validation |
|------------------------|----------|-------------|-----|-----|---------|---------|-----------------|
| id                    | ✓        | INTEGER     |     |     |         |         |                 |
| spot_id              | ✓        | INTEGER     |     |     |         |         |                 |
| user_id              | ✓        | INTEGER     |     |     |         |         |                 |
| parking_timestamp     |          | DATETIME    |     |     |         |         |                 |
| leaving_timestamp    |          | DATETIME    |     |     |         |         |                 |
| parking_cost         |          | FLOAT       |     |     |         |         |                 |



## admin

| Field      | Required | Type        | Min | Max | Default | Pattern | Other Validation |
|-------------|----------|-------------|-----|-----|---------|---------|-----------------|
| id          | ✓        | INTEGER     |     |     |         |         |                 |
| username    |          | VARCHAR(50) |     |     |         |         |                 |
| password    |          | VARCHAR(100)|     |     |         |         |                 |



## user

| Field      | Required | Type        | Min | Max | Default | Pattern | Other Validation |
|-------------|----------|-------------|-----|-----|---------|---------|-----------------|
| id          | ✓        | INTEGER     |     |     |         |         |                 |
| username    |          | VARCHAR(80) |     |     |         |         |                 |
| email       |          | VARCHAR(120)|     |     |         |         |                 |
| password    |          | VARCHAR(200)|     |     |         |         |                 |

## Admin

| Field      | Required | Type     | Min | Max | Default | Pattern | Other Validation |
| ----------- | -------- | -------- | --- | --- | ------- | -------- | ---------------- |
| username   | True     | String   |     | 50  |         |         | Unique            |
| password   |          | String   |     | 100 |         |         |                  |

## Car

| Field          | Required | Type    | Min     | Max     | Default | Pattern | Other Validation |
|-----------------|----------|---------|---------|---------|----------|----------|-------------------|
| licensePlate   | Yes      | String  | 5       |         |          |          |                  |
| year           | Yes      | Integer | 1886    |         |          |          |                  |



## Product

| Field      | Required | Type     | Min     | Max     | Default | Pattern | Other Validation |
|-------------|----------|----------|---------|---------|----------|----------|-------------------|
| name       | Yes      | String   |         |         |          |          |                  |
| price      | Yes      | Number   | 0       |         |          |          | Must be non-negative |



## Inventory

| Field      | Required | Type    | Min | Max | Default | Pattern | Other Validation |
|-------------|----------|---------|-----|-----|----------|----------|-------------------|
| item.name  | Yes      | String  |     |     |          |          | Item must be valid |

