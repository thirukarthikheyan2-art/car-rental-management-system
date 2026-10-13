# PROJECT STATUS

## Completed (Milestones 1-6, all phases implemented)
- M1 Foundation/Admin: fixed delete_car (missing confirmation input), update_car price `<= 0`, write results now checked (add/update/delete return True/False), CSV header guard prevents overwriting a bad file, `create_missing_files()`, cross-role case-insensitive username check (`username_in_use`), 10-digit phone check, car type chosen from list (Hatchback/Sedan/SUV/MPV), login passes the user record to dashboards.
- M2 Customer: book a car, my bookings, details, pay, cancel (own records only).
- M3 Booking: dates.py (manual leap-year/day counting), overlap check, automatic driver assignment, atomic single-write booking.
- M4 Pricing/payments: constants in booking.py, breakdown at booking time, Pending/Paid/Balance Due/Refunded/Not Required.
- M5 Driver/lifecycle: driver dashboard (own assignments only), start/return, late charge, car status Rented/Available (Under Maintenance never overwritten).
- M6 Reports (admin_bookings.py, reports.py), README.md, tests.

## Files created/modified
New: dates.py, booking.py, admin_bookings.py, reports.py, bookings.csv, README.md, tests/test_logic.py.
Modified: main.py, login.py, database.py, admin.py, admin_users.py, customer.py, driver.py.
CSV headers, filenames and existing function names unchanged (dashboards gained an optional `user=""` parameter).
Removed: old README.txt (replaced by README.md), and obsolete `backup/database.py` so it cannot be mistaken for the live database module. `todo-notebook.html` remains in the archive.
- CSV paths are now resolved relative to the folder containing `database.py`, not the terminal's current working directory. This prevents launching the app from another folder from creating or reading a second set of CSV files.

## Design decisions
- No clock access: statuses drive the lifecycle; "before start date" = status Booked.
- Failed-state recovery: car/booking updates are reverted if the second write fails.
- Admin/driver Available/Offline is manual; conflicts come from bookings.

## Tests actually run
- tests/test_logic.py on a copy: 77 passed, 0 failed (dates incl. leap/boundary, pricing, late fee, usernames, overlaps, driver conflicts, payments, cancel, lifecycle).
- Scripted menu sessions via piped input (customer signup/booking/cancel, admin car/driver/booking/report flows, driver dashboard, ownership checks): ran without errors. Output was read by eye, not fully automated.
- Compliance grep for None/raise/class/lambda/map/filter/comprehensions/json/datetime: no violations in the packaged Python files.
- NOT tested: the driver dashboard's availability screen and every report's exact numbers; Windows-specific file locking; Ctrl+D/EOF at prompts raises EOFError (not handled).

## CSV path correction verified
- Launched `main.py` from a different working directory and exited. No CSV files were created in that outside directory.
- `database.get_path()` now points to the single set of CSV files beside `database.py`.
- `bookings.csv` containing only its header means there are currently no saved bookings; it is not a duplicate CSV.

## Remaining / known bugs
- The current uploaded version still does not reject booking start dates in the past; the separate `time.localtime()` correction described in a later checkpoint is not present in this archive.
- Tests mutate CSV records, so run `tests/test_logic.py` only on a disposable copy of the project folder.
- Other limitations are listed in README.md.

## Resume
Read README.md, run `python tests/test_logic.py` in a copy of the folder, then continue from "Remaining".
