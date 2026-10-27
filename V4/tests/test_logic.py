# Logic tests. Run from a COPY of the project folder:  python tests/test_logic.py
# WARNING: the tests REPLACE the CSV files in this folder with small test data
# (tests/fixtures/*.csv), so never run them on your real project folder.
import sys
sys.path.insert(0, ".")

answer = input("Type RESET to replace the CSV data in this folder with test data: ")

if answer != "RESET":
    print("Cancelled. No files were changed.")
    sys.exit()

from database import get_path

for name in ["administrators", "drivers", "customers", "cars", "bookings"]:
    source = open("tests/fixtures/" + name + ".csv", "r", newline="")
    text = source.read()
    source.close()
    target = open(get_path(name), "w", newline="")
    target.write(text)
    target.close()

from dates import is_valid_date, date_to_number, days_between, is_leap_year, days_in_month, get_today
from booking import calculate_price, calculate_late_charge, dates_overlap, create_booking, to_float
from booking import cancel_booking, pay_booking, start_rental, return_rental, find_free_driver
from database import read_table, find_record, username_in_use, update_record, delete_record, create_missing_files, write_table, generate_id
from customer import print_bookable_cars

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed = passed + 1
        print("PASS:", name)
    else:
        failed = failed + 1
        print("FAIL:", name)


def add_days(text, n):
    day = int(text[0:2])
    month = int(text[3:5])
    year = int(text[6:10])

    for i in range(n):
        day = day + 1

        if day > days_in_month(month, year):
            day = 1
            month = month + 1

            if month > 12:
                month = 1
                year = year + 1

    d = str(day)
    m = str(month)

    if len(d) == 1:
        d = "0" + d

    if len(m) == 1:
        m = "0" + m

    return d + "-" + m + "-" + str(year)


TODAY = get_today()
BASE = add_days(TODAY, 10)


def dt(n):
    # dt(1) is 10 days from today, dt(2) the next day, and so on.
    return add_days(BASE, n - 1)


create_missing_files()

# ---- seating capacity filtering ----
cars = read_table("cars")
check("cars have seating capacity field", len(cars) > 0 and "seating_capacity" in cars[0])
check("4-seater filter returns matching cars", print_bookable_cars("4") == 4)
check("6-seater filter returns matching cars", print_bookable_cars("6") == 2)
check("7-seater filter returns matching cars", print_bookable_cars("7") == 3)
check("invalid seating capacity returns no matching cars", print_bookable_cars("5") == 0)

# ---- dates ----
check("leap 2024", is_leap_year(2024))
check("not leap 2100", not is_leap_year(2100))
check("leap 2000", is_leap_year(2000))
check("29-02-2024 valid", is_valid_date("29-02-2024"))
check("29-02-2023 invalid", not is_valid_date("29-02-2023"))
check("29-02-2100 invalid", not is_valid_date("29-02-2100"))
check("31-04-2025 invalid", not is_valid_date("31-04-2025"))
check("31-12-1999 invalid (before 2000)", not is_valid_date("31-12-1999"))
check("00-01-2025 invalid", not is_valid_date("00-01-2025"))
check("1-1-2025 invalid format", not is_valid_date("1-1-2025"))
check("2025-01-01 invalid format", not is_valid_date("2025-01-01"))
check("abc invalid", not is_valid_date("abcdefghij"))
check("empty invalid", not is_valid_date(""))
check("28-02-2024 to 01-03-2024 = 2", days_between("28-02-2024", "01-03-2024") == 2)
check("28-02-2023 to 01-03-2023 = 1", days_between("28-02-2023", "01-03-2023") == 1)
check("01-01-2000 to 01-01-2001 = 366", days_between("01-01-2000", "01-01-2001") == 366)
check("31-12-2025 to 01-01-2026 = 1", days_between("31-12-2025", "01-01-2026") == 1)
check("01-01-2001 to 01-01-2002 = 365", days_between("01-01-2001", "01-01-2002") == 365)
check("same day = 0", days_between("10-05-2026", "10-05-2026") == 0)
check("overlap detected", dates_overlap(dt(1), dt(5), dt(3), dt(8)))
check("same-day handover is not overlap", not dates_overlap(dt(1), dt(5), dt(5), dt(8)))
check("contained overlap", dates_overlap(dt(1), dt(10), dt(3), dt(4)))

# ---- pricing ----
b, d, t = calculate_price(2000, 3, "Self Drive")
check("self drive 3d x 2000 = 6000", b == 6000 and d == 0 and t == 6000)
b, d, t = calculate_price(2000, 3, "With Driver")
check("with driver 3d = 6000 + 1500", d == 1500 and t == 7500)
check("late charge 2d x 2000 x 1.5 = 6000", calculate_late_charge(2000, 2) == 6000)
check("invalid number becomes zero", to_float("not-a-number") == 0.0)
check("NaN is rejected", to_float("nan") == 0.0)
check("positive infinity is rejected", to_float("inf") == 0.0)
check("negative infinity is rejected", to_float("-inf") == 0.0)

# ---- usernames ----
check("admin username taken", username_in_use("admin"))
check("case-insensitive username", username_in_use("ADMIN"))
check("driver username taken", username_in_use("Vijay_Driver"))
check("customer username taken", username_in_use("thiru"))
check("free username", not username_in_use("brandnewname"))
check("own username allowed on edit", not username_in_use("thiru", "customers", "300001"))

# ---- bookings ----
ok, m = create_booking("300001", "400001", dt(1), dt(1), "Self Drive")
check("same-day end rejected", not ok)
ok, m = create_booking("300001", "400001", dt(5), dt(1), "Self Drive")
check("end before start rejected", not ok)
ok, m = create_booking("300001", "400001", "31-02-2026", dt(5), "Self Drive")
check("impossible date rejected", not ok)
ok, m = create_booking("300001", "400006", dt(1), dt(5), "Self Drive")
check("maintenance car rejected", not ok)
ok, m = create_booking("300001", "499999", dt(1), dt(5), "Self Drive")
check("unknown car rejected", not ok)
ok, m = create_booking("399999", "400001", dt(1), dt(5), "Self Drive")
check("unknown customer rejected", not ok)
check("no booking saved by failures", len(read_table("bookings")) == 0)

ok, m = create_booking("300001", "400001", dt(1), dt(5), "Self Drive")
check("first booking ok", ok)
b1 = read_table("bookings")[0]
check("first booking id 500001", b1["booking_id"] == "500001")
check("amount 4 x 1800 = 7200", float(b1["total_amount"]) == 7200)
check("whole total stored without .0", b1["total_amount"] == "7200")
check("new booking Booked/Pending", b1["status"] == "Booked" and b1["payment_status"] == "Pending")
ok, m = create_booking("300002", "400001", dt(3), dt(7), "Self Drive")
check("overlapping booking rejected", not ok)
ok, m = create_booking("300002", "400001", dt(5), dt(7), "Self Drive")
check("same-day handover booking ok", ok)

# driver conflicts: 5 drivers, 2 offline -> 3 available
ok, m = create_booking("300001", "400002", dt(10), dt(12), "With Driver")
check("driver booking ok", ok)
b3 = find_record("bookings", "booking_id", "500003")
check("first available driver assigned", b3["driver_id"] == "200001")
check("driver booking amount 2 x 2000 + 2 x 500 = 5000", float(b3["total_amount"]) == 5000)
ok, m = create_booking("300002", "400003", dt(11), dt(13), "With Driver")
b4 = find_record("bookings", "booking_id", "500004")
check("overlap -> next driver (200002)", ok and b4["driver_id"] == "200002")
ok, m = create_booking("300003", "400007", dt(11), dt(13), "With Driver")
b5 = find_record("bookings", "booking_id", "500005")
check("overlap -> third driver (200004)", ok and b5["driver_id"] == "200004")
before = len(read_table("bookings"))
ok, m = create_booking("300004", "400008", dt(11), dt(13), "With Driver")
check("no driver free -> rejected", not ok)
check("rejected booking not saved", len(read_table("bookings")) == before)
check("car status unchanged after reject", find_record("cars", "car_id", "400008")["status"] == "Available")
ok, m = create_booking("300004", "400008", dt(11), dt(13), "Self Drive")
check("self drive still possible when no driver", ok)

# ---- payments & cancellation ----
ok, m = pay_booking("500001", "300002")
check("other customer cannot pay", not ok)
ok, m = pay_booking("500001", "300001")
check("pay ok", ok and find_record("bookings", "booking_id", "500001")["payment_status"] == "Paid")
ok, m = pay_booking("500001", "300001")
check("double pay rejected", not ok)
ok, m = cancel_booking("500001", "300002")
check("other customer cannot cancel", not ok)
ok, m = cancel_booking("500001", "300001")
r = find_record("bookings", "booking_id", "500001")
check("cancel paid -> Cancelled/Refunded", ok and r["status"] == "Cancelled" and r["payment_status"] == "Refunded")
ok, m = cancel_booking("500001", "300001")
check("double cancel rejected", not ok)
ok, m = pay_booking("500001", "300001")
check("pay cancelled rejected", not ok)
ok, m = cancel_booking("500002", "300002")
r = find_record("bookings", "booking_id", "500002")
check("cancel unpaid -> Not Required", ok and r["payment_status"] == "Not Required")
ok, m = create_booking("300003", "400001", dt(2), dt(4), "Self Drive")
check("cancelled booking frees the car", ok)

# ---- lifecycle ----
ok, m = return_rental("500003", dt(12))
check("return before start rejected", not ok)
ok, m = start_rental("500003", "200002")
check("other driver cannot start", not ok)
ok, m = start_rental("500003", "200001")
check("assigned driver starts", ok and find_record("cars", "car_id", "400002")["status"] == "Rented")
ok, m = start_rental("500003", "200001")
check("double start rejected", not ok)
ok, m = cancel_booking("500003", "300001")
check("cannot cancel ongoing", not ok)
ok, m = return_rental("500003", "31-02-2026", "200001")
check("invalid return date rejected", not ok)
ok, m = return_rental("500003", dt(9), "200001")
check("return before start date rejected", not ok)
ok, m = pay_booking("500003", "300001")
ok, m = return_rental("500003", dt(15), "200001")
r = find_record("bookings", "booking_id", "500003")
check("late 3 days: 5000 + 3 x 2000 x 1.5 = 14000", ok and float(r["total_amount"]) == 14000)
check("late after Paid -> Balance Due", r["payment_status"] == "Balance Due" and r["status"] == "Completed")
check("car Available after return", find_record("cars", "car_id", "400002")["status"] == "Available")
ok, m = return_rental("500003", dt(15), "200001")
check("double return rejected", not ok)
ok, m = pay_booking("500003", "300001")
check("balance paid", ok and find_record("bookings", "booking_id", "500003")["payment_status"] == "Paid")
ok, m = start_rental("500004")
ok, m = return_rental("500004", dt(13))
r = find_record("bookings", "booking_id", "500004")
check("on-time return: no late charge", ok and float(r["total_amount"]) == 2 * 2500 + 2 * 500)
check("on-time unpaid stays Pending", r["payment_status"] == "Pending")

# maintenance car not overwritten by return
ok, m = start_rental("500005")
update_record("cars", "car_id", "400007", {"status": "Under Maintenance"})
ok, m = return_rental("500005", dt(13))
check("return keeps Under Maintenance", ok and find_record("cars", "car_id", "400007")["status"] == "Under Maintenance")

# ---- current-date validation ----
def day_before(text):
    day = int(text[0:2])
    month = int(text[3:5])
    year = int(text[6:10])
    day = day - 1

    if day == 0:
        month = month - 1

        if month == 0:
            month = 12
            year = year - 1

        day = days_in_month(month, year)

    dd = str(day)
    mm = str(month)

    if len(dd) == 1:
        dd = "0" + dd

    if len(mm) == 1:
        mm = "0" + mm

    return dd + "-" + mm + "-" + str(year)


check("get_today is a valid date", is_valid_date(TODAY))
check("add_days/day_before are consistent", add_days(day_before(TODAY), 1) == TODAY)
before = len(read_table("bookings"))
ok, m = create_booking("300005", "400009", day_before(TODAY), TODAY, "Self Drive")
check("yesterday start rejected", not ok)
ok, m = create_booking("300005", "400009", "01-01-2000", add_days(TODAY, 1), "Self Drive")
check("year-2000 start rejected", not ok)
check("rejected past bookings not saved", len(read_table("bookings")) == before)
ok, m = create_booking("300005", "400009", TODAY, add_days(TODAY, 2), "Self Drive")
check("today as start date accepted", ok)
ok, m = create_booking("300005", "400010", add_days(TODAY, 1), add_days(TODAY, 3), "Self Drive")
check("tomorrow as start date accepted", ok)
ok, m = create_booking("300005", "400010", add_days(TODAY, 100), add_days(TODAY, 103), "Self Drive")
check("far-future start date accepted", ok)
check("accepted bookings were saved", len(read_table("bookings")) == before + 3)

# ---- empty-table ID defaults (V3 regression checks) ----
# Preserve each table's rows, test the empty-table starting ID, then restore them.
starting_ids = {
    "administrators": ("admin_id", "100001"),
    "drivers": ("driver_id", "200001"),
    "customers": ("customer_id", "300001"),
    "cars": ("car_id", "400001"),
    "bookings": ("booking_id", "500001")
}

for table in starting_ids:
    saved_rows = read_table(table)
    write_table(table, [])
    field, expected_id = starting_ids[table]
    check("empty " + table + " starts ID at " + expected_id, generate_id(table, field) == expected_id)
    write_table(table, saved_rows)

print("")
print("Passed:", passed, "Failed:", failed)
