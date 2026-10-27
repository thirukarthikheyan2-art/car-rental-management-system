# Booking engine: pricing, availability checks, payments and rental lifecycle.

from database import add_record, find_record, generate_id, read_table, update_record
from dates import is_valid_date, date_to_number, days_between, get_today

# ---- Pricing rules (change these numbers to change the rules) ----
DRIVER_CHARGE_PER_DAY = 500
LATE_FEE_MULTIPLIER = 1.5

ACTIVE_STATUSES = ["Booked", "Ongoing"]


def show_money(amount):
    if amount == int(amount):
        return "Rs. " + str(int(amount))

    return "Rs. " + str(round(amount, 2))


def clean_number(amount):
    # Store whole amounts without ".0" (e.g. 7200 instead of 7200.0).
    if amount == int(amount):
        return int(amount)

    return round(amount, 2)


def to_float(text):
    try:
        number = float(text)

        # Reject NaN and infinity so invalid CSV values cannot poison totals.
        if number != number or number == float("inf") or number == float("-inf"):
            return 0.0

        return number
    except (ValueError, TypeError):
        return 0.0


def calculate_price(rate, days, rental_type):
    # Returns (base charge, driver charge, total).
    base = rate * days
    driver_charge = 0

    if rental_type == "With Driver":
        driver_charge = DRIVER_CHARGE_PER_DAY * days

    return base, driver_charge, base + driver_charge


def calculate_late_charge(rate, late_days):
    return rate * LATE_FEE_MULTIPLIER * late_days


def is_active(booking):
    return booking["status"] in ACTIVE_STATUSES


def dates_overlap(start1, end1, start2, end2):
    # A car handed back on the day the next rental starts is NOT an overlap.
    if not (is_valid_date(start1) and is_valid_date(end1)):
        return False

    if not (is_valid_date(start2) and is_valid_date(end2)):
        return False

    if date_to_number(start1) < date_to_number(end2) and date_to_number(start2) < date_to_number(end1):
        return True

    return False


def car_has_active_booking(car_id):
    for b in read_table("bookings"):
        if b["car_id"] == car_id and is_active(b):
            return True

    return False


def driver_has_active_booking(driver_id):
    for b in read_table("bookings"):
        if b["driver_id"] == driver_id and is_active(b):
            return True

    return False


def car_is_free(car_id, start, end):
    for b in read_table("bookings"):
        if b["car_id"] == car_id and is_active(b):
            if dates_overlap(start, end, b["start_date"], b["end_date"]):
                return False

    return True


def find_free_driver(start, end):
    # First driver (in file order) who is Available and has no clashing booking.
    # Returns the driver record, or "" if nobody is free.
    bookings = read_table("bookings")

    for d in read_table("drivers"):
        if d["availability"] != "Available":
            continue

        clash = False

        for b in bookings:
            if b["driver_id"] == d["driver_id"] and is_active(b):
                if dates_overlap(start, end, b["start_date"], b["end_date"]):
                    clash = True
                    break

        if not clash:
            return d

    return ""


def check_booking_request(car_id, start, end, rental_type):
    # Validates a request without saving. Returns (ok, message, driver_id).
    car = find_record("cars", "car_id", car_id)

    if car == "":
        return False, "Car not found.", ""

    if car["status"] == "Under Maintenance":
        return False, "This car is under maintenance and cannot be booked.", ""

    if not is_valid_date(start) or not is_valid_date(end):
        return False, "Invalid date.", ""

    today = get_today()

    if not is_valid_date(today):
        return False, "The computer's system date is outside the supported range; booking dates cannot be checked.", ""

    if date_to_number(start) < date_to_number(today):
        return False, "Start date cannot be in the past (today is " + today + ").", ""

    if date_to_number(end) <= date_to_number(start):
        return False, "End date must be later than the start date.", ""

    if rental_type != "Self Drive" and rental_type != "With Driver":
        return False, "Invalid rental type.", ""

    if to_float(car["price_per_day"]) <= 0:
        return False, "This car has no valid price and cannot be booked.", ""

    if not car_is_free(car_id, start, end):
        return False, "This car is already booked for part of that period.", ""

    driver_id = ""

    if rental_type == "With Driver":
        driver = find_free_driver(start, end)

        if driver == "":
            return False, "No driver is available for that period.", ""

        driver_id = driver["driver_id"]

    return True, "OK", driver_id


def new_booking_id():
    if len(read_table("bookings")) == 0:
        return "500001"

    return generate_id("bookings", "booking_id")


def create_booking(customer_id, car_id, start, end, rental_type):
    # Saves one booking. Returns (ok, message). Nothing is saved if any check fails.
    if find_record("customers", "customer_id", customer_id) == "":
        return False, "Customer not found."

    ok, message, driver_id = check_booking_request(car_id, start, end, rental_type)

    if not ok:
        return False, message

    car = find_record("cars", "car_id", car_id)
    days = days_between(start, end)
    base, driver_charge, total = calculate_price(to_float(car["price_per_day"]), days, rental_type)
    booking_id = new_booking_id()

    saved = add_record("bookings", {
        "booking_id": booking_id,
        "customer_id": customer_id,
        "car_id": car_id,
        "start_date": start,
        "end_date": end,
        "rental_type": rental_type,
        "driver_id": driver_id,
        "total_amount": clean_number(total),
        "status": "Booked",
        "payment_status": "Pending"
    })

    if not saved:
        return False, "Booking could not be saved."

    return True, "Booking confirmed! Your Booking ID is " + booking_id


def get_booking_for(booking_id, customer_id="", driver_id=""):
    # Returns the booking, or "" if it does not exist or belongs to someone else.
    b = find_record("bookings", "booking_id", booking_id)

    if b == "":
        return ""

    if customer_id != "" and b["customer_id"] != customer_id:
        return ""

    if driver_id != "" and b["driver_id"] != driver_id:
        return ""

    return b


def cancel_booking(booking_id, customer_id=""):
    # Only a booking that has not started (status Booked) can be cancelled.
    b = get_booking_for(booking_id, customer_id)

    if b == "":
        return False, "Booking not found."

    if b["status"] == "Cancelled":
        return False, "This booking is already cancelled."

    if b["status"] == "Completed":
        return False, "A completed booking cannot be cancelled."

    if b["status"] == "Ongoing":
        return False, "The rental has already started and cannot be cancelled."

    if b["payment_status"] == "Paid":
        new_payment = "Refunded"
        message = "Booking cancelled. Full refund of " + show_money(to_float(b["total_amount"])) + " (simulated)."
    else:
        new_payment = "Not Required"
        message = "Booking cancelled. No payment had been made."

    if update_record("bookings", "booking_id", booking_id,
                     {"status": "Cancelled", "payment_status": new_payment}):
        return True, message

    return False, "Booking could not be cancelled."


def pay_booking(booking_id, customer_id=""):
    b = get_booking_for(booking_id, customer_id)

    if b == "":
        return False, "Booking not found."

    if b["status"] == "Cancelled":
        return False, "A cancelled booking cannot be paid."

    if b["payment_status"] == "Paid":
        return False, "This booking is already fully paid."

    if b["payment_status"] != "Pending" and b["payment_status"] != "Balance Due":
        return False, "No payment is due for this booking."

    if update_record("bookings", "booking_id", booking_id, {"payment_status": "Paid"}):
        return True, "Payment received (simulated)."

    return False, "Payment could not be recorded."


def start_rental(booking_id, driver_id=""):
    b = get_booking_for(booking_id, "", driver_id)

    if b == "":
        return False, "Booking not found."

    if b["status"] != "Booked":
        return False, "Only a booking with status Booked can be started (current status: " + b["status"] + ")."

    car = find_record("cars", "car_id", b["car_id"])

    if car == "":
        return False, "The car for this booking no longer exists."

    if car["status"] != "Available":
        return False, "The car is not available right now (status: " + car["status"] + ")."

    if not update_record("cars", "car_id", b["car_id"], {"status": "Rented"}):
        return False, "Could not update the car."

    if not update_record("bookings", "booking_id", booking_id, {"status": "Ongoing"}):
        update_record("cars", "car_id", b["car_id"], {"status": "Available"})
        return False, "Could not start the rental."

    return True, "Rental started. Car is now marked Rented."


def return_rental(booking_id, return_date, driver_id=""):
    b = get_booking_for(booking_id, "", driver_id)

    if b == "":
        return False, "Booking not found."

    if b["status"] != "Ongoing":
        return False, "Only an Ongoing rental can be returned (current status: " + b["status"] + ")."

    if not is_valid_date(return_date):
        return False, "Invalid return date."

    if date_to_number(return_date) < date_to_number(b["start_date"]):
        return False, "Return date cannot be before the start date."

    total = to_float(b["total_amount"])
    payment = b["payment_status"]
    message = "Rental completed."
    car = find_record("cars", "car_id", b["car_id"])

    if date_to_number(return_date) > date_to_number(b["end_date"]):
        late_days = days_between(b["end_date"], return_date)
        rate = 0.0

        if car != "":
            rate = to_float(car["price_per_day"])

        late_charge = calculate_late_charge(rate, late_days)
        total = total + late_charge
        message = message + " Late by " + str(late_days) + " day(s). Late charge: " + show_money(late_charge) + "."

        if payment == "Paid":
            payment = "Balance Due"

    carry_on = True

    if car != "" and car["status"] == "Rented":
        carry_on = update_record("cars", "car_id", b["car_id"], {"status": "Available"})

    if not carry_on:
        return False, "Could not update the car."

    changes = {"status": "Completed", "total_amount": clean_number(total), "payment_status": payment}

    if not update_record("bookings", "booking_id", booking_id, changes):
        if car != "" and car["status"] == "Rented":
            update_record("cars", "car_id", b["car_id"], {"status": "Rented"})

        return False, "Could not complete the rental."

    message = message + " Total amount: " + show_money(total) + "."

    if payment == "Balance Due":
        message = message + " Balance due - the customer must pay again."

    return True, message


# ---------------- display helpers ----------------

def car_label(car_id):
    car = find_record("cars", "car_id", car_id)

    if car == "":
        return "(deleted car " + car_id + ")"

    return car["model"]


def person_name(table, id_field, person_id):
    if person_id == "":
        return "-"

    p = find_record(table, id_field, person_id)

    if p == "":
        return "(removed " + person_id + ")"

    return p["name"]


def print_booking_line(b):
    if b is None:
        return
    print("{:<12} {:<22} {:<23} {:<13} {:>12} {:<12} {:<14}".format(
        b["booking_id"], car_label(b["car_id"]),
        b["start_date"] + " to " + b["end_date"], b["rental_type"],
        show_money(to_float(b["total_amount"])), b["status"], b["payment_status"]))


def print_booking_details(b, show_customer=False):
    print("------------------------------")
    print("Booking ID:", b["booking_id"])

    if show_customer:
        cust = find_record("customers", "customer_id", b["customer_id"])
        print("Customer:", person_name("customers", "customer_id", b["customer_id"]))

        if cust != "":
            print("Customer Phone:", cust["phone"])

    print("Car:", car_label(b["car_id"]), "(ID " + b["car_id"] + ")")
    print("Start Date:", b["start_date"])
    print("End Date:", b["end_date"])
    print("Rental Type:", b["rental_type"])

    if b["driver_id"] != "":
        print("Driver:", person_name("drivers", "driver_id", b["driver_id"]))

    print("Total Amount:", show_money(to_float(b["total_amount"])))
    print("Booking Status:", b["status"])
    print("Payment Status:", b["payment_status"])
    print("------------------------------")
