# Validation Documentation: parking_app

## advanced_tests/cross_file_main.py
## Person

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age | Yes | Integer | 0 |  |  |  | Must be a non-negative integer.  |


## advanced_tests/cross_file_utils.py
## User

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age |  | integer | 0 |  |  |  |  Must be non-negative |


## advanced_tests/decorator_validation.py
## UserModel

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| email |  | str |  |  | ✓ |  | must contain @ |
| age |  | int | 0 |  |  |  | must be positive |


## advanced_tests/dynamic_fields.py
## DynamicUser

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| age |  |  | 0 |  |  |  | Must be positive |
|  |  |  |  |  |  |  |  |

> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete.


## advanced_tests/java_dynamic.java
## AdvancedValidationCar

| Field             | Required | Type      | Min      | Max      | Email    | Pattern                      | Other Validation |
|----------------------|----------|-----------|-----------|-----------|----------|------------------------------|-----------------|
| vin                | Yes      | String    |           |           |          |                              |                  |
| ownerName          | Yes      | String    |           |           |          |                              |                  |
| licensePlate       |          | String    |           |           |          | `[A-Z]{2}[0-9]{2} [A-Z]{3}` |                  |
| year               |          | Integer   | 1886      | 2100      |          |                              |                  |
| modelName          |          | String    | 2         | 30        |          |                              |                  |
| contactEmail       |          | String    |           |           | Yes      |                              |                  |
| numberOfDoors      |          | Integer   | 1         |           |          |                              |                  |
| numberOfPreviousOwners |          | Integer   | 0         |           |          |                              |                  |
| negativeTestValue  |          | Integer   |           |           |          |                              |                  |
| negativeOrZeroTestValue |          | Integer   |           | 0         |          |                              |                  |
| registrationDate   |          | LocalDate |           |           |          |                              | Past             |
| lastServiceDate    |          | LocalDate |           |           |          |                              | PastOrPresent    |
| insuranceExpiryDate |          | LocalDate |           |           |          |                              | Future           |
| warrantyExpiryDate  |          | LocalDate |           |           |          |                              | FutureOrPresent  |
| price              |          | BigDecimal| 0.0       | 1000000.0 |          |                              |                  |
| engineCapacity     |          | BigDecimal|           |           |          |                              | Digits(5,2)      |
| isInsured          |          | Boolean   |           |           |          |                              | AssertTrue       |
| isStolen           |          | Boolean   |           |           |          |                              | AssertFalse      |


## DynamicCar

No validation rules are explicitly defined within this class.  Validation would need to be implemented dynamically, outside the scope of static analysis.


## advanced_tests/js.dynamic.js
## DynamicObj

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| field_X  |  |  |  |  |  |  |  Value assigned dynamically; no inherent validation in the class |


## app.py
## Authentication (Assuming validation exists within `auth_bp` -  details not provided)

| Field        | Required | Type      | Min | Max | Email | Pattern        | Other Validation |
|--------------|----------|-----------|-----|-----|-------|-----------------|-------------------|
| username     |           |           |     |     |       |                 |                   |
| password     |           |           |     |     |       |                 |                   |
| email        |           |           |     |     |       |                 |                   |


## Parking (Assuming validation exists within `parking_bp` and `models` - details not provided)

| Field        | Required | Type      | Min | Max | Email | Pattern        | Other Validation |
|--------------|----------|-----------|-----|-----|-------|-----------------|-------------------|
| license_plate|           |           |     |     |       |                 |                   |
| entry_time   |           |           |     |     |       |                 |                   |
| exit_time    |           |           |     |     |       |                 |                   |
| parking_spot|           |           |     |     |       |                 |                   |


## controllers/auth.py
## User Registration Form

| Field      | Required | Type      | Min | Max | Email | Pattern | Other Validation                                 |
|-------------|----------|-----------|-----|-----|-------|---------|-------------------------------------------------|
| username   | Yes      | String    |     |     |       |         | Must be unique                               |
| email      | Yes      | String    |     |     | Yes   |         | Must be unique                               |
| password   | Yes      | String    |     |     |       |         |                                                 |


## User Login Form

| Field      | Required | Type      | Min | Max | Email | Pattern | Other Validation                    |
|-------------|----------|-----------|-----|-----|-------|---------|---------------------------------------|
| username   | Yes      | String    |     |     |       |         |                                       |
| password   | Yes      | String    |     |     |       |         | Must match stored password in database |


## controllers/parking_controller.py
## ParkingLot

| Field                | Required | Type             | Min | Max | Other Validation                                           |
|-----------------------|----------|-------------------|-----|-----|-----------------------------------------------------------|
| prime_location_name | ✓        | String           |     |     |                                                           |
| price_per_hour       | ✓        | Float/Integer     |     |     | Must be non-negative                                      |
| address              | ✓        | String           |     |     |                                                           |
| pin_code             | ✓        | String/Integer   |     |     |                                                           |
| max_number_of_spots  | ✓        | Integer          | 1   |     | Must be a positive integer                               |


## ParkingSpot

| Field         | Required | Type    | Min | Max | Other Validation |
|-----------------|----------|---------|-----|-----|--------------------|
| lot_id        | ✓        | Integer |     |     |                   |
| spot_number   | ✓        | String  |     |     |                   |
| status        | ✓        | String  |     |     | Value must be 'A' or 'O' |


## Reservation

| Field               | Required | Type             | Min | Max | Other Validation                                      |
|-----------------------|----------|-------------------|-----|-----|------------------------------------------------------|
| spot_id              | ✓        | Integer          |     |     |                                                      |
| user_id              | ✓        | Integer          |     |     |                                                      |
| parking_timestamp    | ✓        | DateTime         |     |     |                                                      |
| leaving_timestamp    |         | DateTime         |     |     |                                                      |
| parking_cost         |         | Float/Integer     |     |     | Must be non-negative                                  |


## User

| Field     | Required | Type    | Min | Max | Email       | Other Validation |
|------------|----------|---------|-----|-----|-------------|-----------------|
| id         | ✓        | Integer |     |     |             |                 |
| username   | ✓        | String  |     |     |             |                 |
| email      | ✓        | String  |     |     | ✓           |                 |

> **Note:** This file uses dynamic field creation (e.g., `setattr`). Static analysis may be incomplete.


## models/admin.py
## Admin

| Field      | Required | Type      | Min | Max | Unique | Other Validation |
| ----------- | -------- | ---------- | --- | --- | ------ | --------------- |
| username   | Yes       | String     |     | 50  | Yes    |                  |
| password   | Yes       | String     |     | 100 |       |                  |


## models/parking_lot.py
## ParkingLot

| Field                  | Required | Type     | Min | Max | Email | Pattern | Other Validation |
|--------------------------|----------|----------|-----|-----|-------|---------|--------------------|
| prime_location_name     | Yes      | String   |     | 100 |       |         |                    |
| price_per_hour          | Yes      | Float    |     |     |       |         |                    |
| address                 | Yes      | String   |     | 200 |       |         |                    |
| pin_code                | Yes      | String   |     | 10  |       |         |                    |
| max_number_of_spots     | Yes      | Integer  |     |     |       |         |                    |


## models/parking_spot.py
## ParkingSpot

| Field         | Required | Type     | Min | Max | Email | Pattern | Other Validation |
|-----------------|----------|----------|-----|-----|-------|---------|-----------------|
| lot_id         | Yes      | Integer  |      |      |       |         |                 |
| spot_number    | Yes      | String   |      | 10  |       |         |                 |
| status         | Yes      | String   |      | 1   |       |         | Must be 'A' or 'O' |


## models/reservation.py
## Reservation

| Field             | Required | Type      | Min      | Max      | Email | Pattern | Other Validation             |
|-----------------|----------|-----------|-----------|-----------|-------|---------|-----------------------------|
| spot_id          | Yes      | Integer   |           |           |       |         | Must be a valid foreign key |
| user_id          | Yes      | Integer   |           |           |       |         | Must be a valid foreign key |
| parking_timestamp| No       | DateTime  |           |           |       |         | Must be a valid datetime    |
| leaving_timestamp| No       | DateTime  |           |           |       |         | Must be a valid datetime if present |
| parking_cost     | No       | Float     |           |           |       |         |                             |


## models/test.py
## User

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes | str |  |  |  |  |  |
| age | No | int | 0 |  |  |  |  |
| email | Yes | str |  |  | Yes |  | Must contain "@" |
| password | Yes | str | 8 |  |  |  |  |


## Admin

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes | str |  |  |  |  |  |
| age | No | int | 0 |  |  |  |  |
| email | Yes | str |  |  | Yes |  | Must contain "@" |
| access_level | Yes | int | 1 | 10 |  |  |  |


## Car

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| licensePlate | Yes | String | 5 |  |  |  |  |
| year | Yes | int | 1886 |  |  |  |  |


## Product

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes |  |  |  |  |  |  |
| price | Yes | Number | 0 |  |  |  | Must be non-negative |


## Inventory

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| item | Yes | Object |  |  |  |  | Must have a name property |


## models/user.py
## User

| Field      | Required | Type      | Min | Max | Unique | Other Validation |
| ----------- | -------- | ---------- | --- | --- | ------- | ---------------- |
| username   | Yes       | String     |     | 80  | Yes     |                  |
| email      | Yes       | String     |     | 120 | Yes     |                  |
| password   | Yes       | String     |     | 200 |        |                  |


## templates/app.py
## No validation logic found in provided code.


## templates/home.html
## No Validation Found

No validation logic was found in the provided code.


## templates/login.html
## Login Form

| Field   | Required | Type      | Min | Max | Email | Pattern | Other Validation |
| :------ | :------- | :-------- | :-: | :-: | :---- | :------ | :---------------- |
| email   | Yes      |          |     |     | Yes   |         |                    |
| password | Yes      |          |     |     |      |         |                    |


## templates/register.html
## Register Form

| Field | Required | Type | Min | Max | Email | Pattern | Other Validation |
|---|---|---|---|---|---|---|---|
| name | Yes |  |  |  |  |  |  |
| email | Yes |  |  |  | Yes |  |  |
| password | Yes |  |  |  |  |  |  |
