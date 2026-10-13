# Administrator reports, calculated from the stored CSV records.

from database import read_table
from booking import show_money, to_float
from dates import days_between, is_valid_date


def booking_summary():
    print("========== BOOKING SUMMARY ==========")
    bookings = read_table("bookings")
    statuses = ["Booked", "Ongoing", "Completed", "Cancelled"]
    print("Total bookings:", len(bookings))

    for st in statuses:
        count = 0

        for b in bookings:
            if b["status"] == st:
                count = count + 1

        print(st + ":", count)

    self_drive = 0
    with_driver = 0

    for b in bookings:
        if b["rental_type"] == "Self Drive":
            self_drive = self_drive + 1
        elif b["rental_type"] == "With Driver":
            with_driver = with_driver + 1

    print("Self Drive:", self_drive, "| With Driver:", with_driver)
    input("Press Enter to continue...")


def revenue_summary():
    print("========== REVENUE & PAYMENTS ==========")
    paid_total = 0.0
    pending_total = 0.0
    refunded_total = 0.0
    paid_count = 0
    pending_count = 0
    balance_count = 0
    balance_total = 0.0
    refunded_count = 0

    for b in read_table("bookings"):
        amount = to_float(b["total_amount"])

        if b["payment_status"] == "Paid":
            paid_total = paid_total + amount
            paid_count = paid_count + 1
        elif b["payment_status"] == "Pending":
            pending_total = pending_total + amount
            pending_count = pending_count + 1
        elif b["payment_status"] == "Balance Due":
            balance_total = balance_total + amount
            balance_count = balance_count + 1
        elif b["payment_status"] == "Refunded":
            refunded_total = refunded_total + amount
            refunded_count = refunded_count + 1

    print("Fully paid bookings:", paid_count, "| Revenue:", show_money(paid_total))
    print("Payment pending:", pending_count, "| Amount:", show_money(pending_total))
    print("Balance due (late charge unpaid):", balance_count, "| Total booking value:", show_money(balance_total))
    print("Refunded:", refunded_count, "| Amount:", show_money(refunded_total))
    input("Press Enter to continue...")


def car_utilisation():
    print("========== CAR UTILISATION ==========")
    print("(Cancelled bookings are not counted)")
    bookings = read_table("bookings")
    cars = read_table("cars")

    if len(cars) == 0:
        print("No cars found.")

    for c in cars:
        count = 0
        days = 0

        for b in bookings:
            if b["car_id"] == c["car_id"] and b["status"] != "Cancelled":
                count = count + 1

                if is_valid_date(b["start_date"]) and is_valid_date(b["end_date"]):
                    days = days + days_between(b["start_date"], b["end_date"])

        print(c["car_id"], c["model"], "| Status:", c["status"], "| Bookings:", count, "| Booked days:", days)

    input("Press Enter to continue...")


def driver_summary():
    print("========== DRIVER ASSIGNMENTS ==========")
    bookings = read_table("bookings")
    drivers = read_table("drivers")

    if len(drivers) == 0:
        print("No drivers found.")

    for d in drivers:
        total = 0
        active = 0

        for b in bookings:
            if b["driver_id"] == d["driver_id"] and b["status"] != "Cancelled":
                total = total + 1

                if b["status"] == "Booked" or b["status"] == "Ongoing":
                    active = active + 1

        print(d["driver_id"], d["name"], "|", d["availability"], "| Assignments:", total, "| Active:", active)

    input("Press Enter to continue...")


def reports_menu():
    while True:
        print("==============================")
        print("            REPORTS")
        print("==============================")
        print("1. Booking Summary")
        print("2. Revenue and Payments")
        print("3. Car Utilisation")
        print("4. Driver Assignments")
        print("5. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            booking_summary()
        elif choice == "2":
            revenue_summary()
        elif choice == "3":
            car_utilisation()
        elif choice == "4":
            driver_summary()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
