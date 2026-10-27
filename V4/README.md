# Car Rental Management System — V4

Class 12 CBSE Computer Science project implemented in Python with CSV-based storage.

## Requirements

- Python 3.10 or newer (the project uses only the Python standard library).
- Windows, macOS, or Linux terminal.

## Run the application on Windows

1. Extract the complete `car_rental_V3.zip` archive.
2. Open the extracted `car_rental_V3` folder in VS Code.
3. Open `main.py` and choose **Run Python File in Terminal**, or open a terminal in this folder and run:

   ```powershell
   python main.py
   ```

Run `main.py`, not a `.csv` file. CSV files are data files and cannot be executed as Python programs.

## Data files

The application reads and writes these CSV files from the project folder:

- `administrators.csv`
- `drivers.csv`
- `customers.csv`
- `cars.csv`
- `bookings.csv`

Keep the headers unchanged. Make a backup before editing the demo records manually. The program creates a missing CSV file with its header, but it does not replace an existing file with an invalid header.

## Run the logic tests safely

**The test script replaces the CSV files in the folder where it runs with test fixture data. Do not run it in your only working/demo copy.**

1. Make a separate copy of the extracted project folder.
2. Open a terminal in that copied folder.
3. Run:

   ```powershell
   python tests/test_logic.py
   ```

4. Type `RESET` only when you are sure you are in the disposable test copy.

The current logic test suite reports 96 passed and 0 failed. Results may differ if the code or fixtures are changed.

## Main modules

- `main.py`: entry point and top-level menu.
- `login.py`: role selection, login, and customer sign-up navigation.
- `admin.py`: administrator dashboard and car management.
- `admin_users.py`: driver and user management.
- `admin_bookings.py`: administrator booking operations.
- `customer.py`: customer portal and registration.
- `driver.py`: driver portal and assigned rental operations.
- `booking.py`: booking validation, pricing, driver assignment, payment status, cancellation, start and return logic.
- `dates.py`: manual date validation and day calculations; `time.localtime()` is used to read the computer's current local date.
- `database.py`: shared CSV read/write/search/update/delete functions.
- `reports.py`: booking, payment, car-use, and driver summaries.

## Known limitations

- Passwords are stored as plain text in the CSV files; this is a school demonstration, not production-grade security.
- Payments and refunds are simulated status updates. No money is transferred.
- CSV storage does not provide database transactions, relational constraints, or safe concurrent multi-user writes.
- `Balance Due` reports show the total booking value associated with those bookings, not a separately stored exact unpaid amount.
- Driver availability is manually managed; assignment conflicts are also checked against active bookings.
- The app relies on the computer's system date and clock.


## Seating capacity filtering
Cars now include a `seating_capacity` field (4, 6, or 7). Administrators select it when adding a car and can change it through Update Car. Customers choose a seating capacity before selecting a car to book. When an older `cars.csv` is first read, the program preserves a backup as `cars.csv.backup` and migrates the old rows; legacy cars default to 4 seats, so administrators should verify each existing car's actual capacity through Update Car.


## V4 terminal table formatting

V4 uses Python `str.format()` to align tabular terminal output for cars, bookings, drivers, users, and report listings. This uses Python built-in string formatting and does not require external packages.
