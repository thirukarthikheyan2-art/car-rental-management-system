# V3 Debugging and Verification Report

## Scope

Audited the supplied V2 source files, CSV headers and demo records; compiled all Python modules; ran the included logic tests on a disposable copy; and made the targeted corrections listed below.

## Corrections in V3

1. **ID generation for empty tables:** `generate_id()` now preserves the project's ID ranges when a table is empty: administrators `100001`, drivers `200001`, customers `300001`, cars `400001`, and bookings `500001`. Previously, empty tables could generate the generic ID `1`, inconsistent with the existing data.
2. **Admin setting an assigned driver Offline:** `admin_users.update_driver()` now prevents setting a driver Offline when that driver has Booked or Ongoing assignments. The driver portal already had a corresponding restriction; this makes the administrative route consistent.
3. **Added a root README:** the supplied archive did not include the README described in its project status. V3 includes Windows run instructions, safe test instructions, module descriptions and known limitations.
4. **Removed repository/runtime clutter from the deliverable:** the V3 archive excludes `.git`, `__pycache__`, and `.pyc` files. Source, CSV demo data, fixtures, tests, project status and the existing notebook HTML are retained.

## Checks performed

- Python compilation: all project `.py` files and `tests/test_logic.py` compile successfully.
- Baseline V2 logic tests: **87 passed, 0 failed** on a disposable copy. V3 adds nine regression checks and now reports **96 passed, 0 failed**, after entering the test script's required `RESET` confirmation.
- CSV shape: all five data CSV files have the expected header and every row has the expected number of columns.
- Demo-data integrity: no duplicate IDs, no duplicate usernames across user roles, no invalid 10-digit phone values, no missing customer/car/driver references in bookings, no overlapping active car or driver assignments, and no detected booking-price inconsistencies under the project's stated pricing rules.
- The tests were run on a separate copy because the test script intentionally replaces CSV files with fixtures.

## Remaining limitations (not silently presented as fixed)

- Plain-text passwords remain a security weakness.
- CSV writes are not transactional and the application is not designed for simultaneous writers.
- Payments/refunds are simulated.
- The schema does not separately store the exact unpaid balance after a late return, so the report labels the full booking value for `Balance Due` records.
- The application depends on the host computer's system date.
- The test suite does not establish that every possible user interaction or Windows file-locking scenario is error-free.

## How to run

From the extracted `car_rental_V3` folder, run `python main.py`. Do not run a CSV file. To run tests, first make a disposable copy, then run `python tests/test_logic.py` and type `RESET` only in that copy.

5. **Non-finite prices/numbers:** `admin.ask_price()` now rejects `NaN` and positive/negative infinity, which Python can otherwise parse as floats despite them not being valid real prices. `booking.to_float()` maps invalid, NaN and infinite values to `0.0` so they cannot contaminate price/revenue calculations.
6. **Unsupported computer date:** booking validation now rejects the request if the computer's system date falls outside the project's supported 2000–2100 range. Previously, the past-date comparison could be skipped if the system date itself failed the project's date validator.
7. **Additional regression tests:** four checks cover invalid/NaN/infinite numeric values. The five empty-table ID tests remain. Total included suite: **96 passed, 0 failed** on a disposable copy.
8. **Administrative availability guard verified:** a scripted smoke test confirmed an administrator cannot set a driver Offline while that driver has a Booked assignment.
