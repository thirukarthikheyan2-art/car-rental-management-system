# Project Status — V3

## V3 corrections
- `database.generate_id()` preserves the existing ID ranges when a table is empty: administrators 100001, drivers 200001, customers 300001, cars 400001, bookings 500001.
- `admin_users.update_driver()` now prevents an administrator from setting a driver Offline while that driver has a Booked or Ongoing assignment. This matches the restriction in the driver's own availability menu.
- Added `README.md` with Windows launch and safe test instructions.
- Added `V3_AUDIT_REPORT.md` with verification scope, results, fixes, and remaining limitations.
- Added regression checks for the empty-table ID defaults.

## Verification
- All Python source files and the test script compile.
- The original supplied logic suite passed 87/87 before V3 changes.
- V3 suite includes four additional non-finite-number checks and five empty-table ID checks; it reports 96 passed, 0 failed on a disposable project copy.
- CSV demo data was checked for expected headers/row widths, unique IDs and usernames, valid phone formats, valid booking references, non-overlapping active car/driver assignments, and pricing consistency. No integrity issues were found in those checks.

## Known limitations
- Passwords are stored as plain text.
- Payments/refunds are simulated status changes, not real transactions.
- CSV storage has no relational constraints or transactional multi-file updates and is not intended for concurrent writers.
- The Balance Due report shows the full booking value for those bookings, not a separately stored exact unpaid balance.
- Driver availability is manually managed, with active booking conflicts checked separately.
- The program relies on the computer's local system date.
- A complete exhaustive proof of all possible runtime behaviour and Windows file-locking scenarios is not possible from the current test suite.

## Safe usage
- Run the program from this folder with `python main.py`.
- Do not run CSV files as Python programs.
- `tests/test_logic.py` replaces CSVs with test fixture data after the user types `RESET`. Run it only in a disposable copy, never in the only copy of the demo data.
