# Car Rental Management System (CBSE Class 12 CS Project)

Command-line Python 3 project using CSV files for storage. Standard library only (`csv`).

## Run
Open a terminal **inside this folder** and run: `python main.py`
(Missing CSV files are created automatically with their headers.)

## Features
- Roles: Administrator, Driver, Customer (customers can sign up).
- Usernames are unique across all roles (capital letters ignored).
- Administrator: add/update/delete cars and drivers, view users, manage bookings (view, start, return, cancel), reports.
- Customer: browse cars, view details, book a car (self-drive or with driver), see price breakdown, view own bookings, pay (simulated), cancel before the rental starts.
- Driver: see own assignments, start/complete own rentals, set own availability.
- Reports: booking summary, revenue/payments, car utilisation, driver assignments.

## Rules
- Dates are DD-MM-YYYY (years 2000-2100). Rental days = end date - start date; the end date must be later than the start date.
- Price = days x car's daily rate. With a driver: + Rs. 500 per day (`DRIVER_CHARGE_PER_DAY` at the top of `booking.py`).
- A car cannot be booked for overlapping dates. Returning a car on the day the next rental starts is allowed.
- Driver: the first driver whose availability is "Available" and who has no clashing booking is assigned automatically. If none is free the booking is rejected and nothing is saved.
- Booking status: Booked -> Ongoing -> Completed, or Booked -> Cancelled.
- Payment status: Pending -> Paid. Cancelling a Paid booking before it starts -> Refunded (simulated, full refund). Cancelling an unpaid booking -> Not Required.
- Late return: if the actual return date is after the end date, the extra charge is 1.5 x the car's daily rate for each extra day (`LATE_FEE_MULTIPLIER` in `booking.py`). It is added to the total amount. If the booking was already Paid, payment status becomes "Balance Due" and the customer pays again.
- Cars/drivers with Booked or Ongoing rentals cannot be deleted. A car with active rentals cannot have its price or maintenance status changed.

## Files
| File | Purpose |
|---|---|
| main.py | Start-up and main menu |
| login.py | Login; passes the logged-in user to the dashboard |
| database.py | CSV read/write helpers, IDs, username and phone checks |
| dates.py | DD-MM-YYYY validation and day counting |
| booking.py | Pricing, overlap checks, driver assignment, payment, start/return/cancel |
| admin.py, admin_users.py, admin_bookings.py, reports.py | Administrator features |
| customer.py | Customer features and sign-up |
| driver.py | Driver features |
| tests/test_logic.py | Automated logic tests (run on a copy of the folder) |

CSV files: `administrators.csv`, `drivers.csv`, `customers.csv`, `cars.csv`, `bookings.csv` (column names are the first row of each file).

## Demo accounts (records in the CSV files are demo data)
Admin `admin`/`admin123`, Driver `vijay_driver`/`vijay123`, Customer `thiru`/`thiru123`.

## Known limitations
- Passwords are stored as plain text in the CSV files (school project; no hashing library used). Passwords are never displayed.
- The program does not read the computer clock: start/return are processed by a driver or administrator, and the actual return date is typed in. Past start dates are therefore not rejected.
- A Completed booking's total includes any late charge, which is stored only as part of the total.
- "Balance Due" revenue is reported as the total booking value, because the already-paid part is not stored separately.
- Driver "Available/Offline" is set manually; clashes are decided from bookings.
- Run `tests/test_logic.py` on a copy of the folder, because it writes test bookings.


### CSV file locations

The program reads and writes the CSV files stored beside `database.py` in the project folder. File paths are based on the location of the program, not the terminal's current working directory. This prevents a second set of empty CSV files from being created when the program is launched from another folder. Keep one copy of each data CSV in the project folder.
