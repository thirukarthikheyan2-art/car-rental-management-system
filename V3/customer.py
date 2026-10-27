
from database import add_record, find_record, generate_id, read_table, username_in_use, valid_phone
from booking import calculate_price, check_booking_request, create_booking, cancel_booking, pay_booking
from booking import print_booking_line, print_booking_details, get_booking_for, show_money, to_float
from booking import DRIVER_CHARGE_PER_DAY
from dates import ask_date, days_between


def view_available_cars():
    print("==============================================================")
    print("                    AVAILABLE CARS")
    print("==============================================================")

    cars = read_table("cars")
    count = 0

    print("ID\tMODEL\t\tTYPE\t\tSEATS\tPRICE/DAY")
    print("--------------------------------------------------------------")

    for car in cars:
        if car["status"].lower() == "available":
            print(
                car["car_id"],
                "\t",
                car["model"],
                "\t",
                car["car_type"],
                "\t", car.get("seating_capacity", "4"),
                "\tRs.",
                car["price_per_day"]
            )
            count = count + 1

    if count == 0:
        print("No cars are currently available.")

    input("Press Enter to continue...")

def view_car_details():
    print("==============================")
    print("        CAR DETAILS")
    print("==============================")

    cars = read_table("cars")

    if len(cars) == 0:
        print("No cars found.")
        input("Press Enter to continue...")
        return

    car_id = input("Enter Car ID: ").strip()
    found = False

    for car in cars:
        if car["car_id"] == car_id:
            found = True

            print("------------------------------")
            print("Car ID:", car["car_id"])
            print("Model:", car["model"])
            print("Type:", car["car_type"])
            print("Seating Capacity:", car.get("seating_capacity", "4"))
            print("Price per Day: Rs.", car["price_per_day"])
            print("Status:", car["status"])
            print("------------------------------")

            break

    if not found:
        print("Car not found.")

    input("Press Enter to continue...")


def choose_seating_capacity():
    while True:
        print("1. 4-seater")
        print("2. 6-seater")
        print("3. 7-seater")
        print("B. Go back")
        choice = input("Choose seating capacity: ").strip().lower()

        if choice == "1":
            return "4"
        elif choice == "2":
            return "6"
        elif choice == "3":
            return "7"
        elif choice == "b":
            return ""
        else:
            print("Enter 1, 2, 3 or B.")


def print_bookable_cars(seating_capacity):
    cars = read_table("cars")
    count = 0

    print("ID\tMODEL\t\tTYPE\t\tSEATS\tPRICE/DAY\tSTATUS")
    print("--------------------------------------------------------------------------")

    for car in cars:
        if car["status"] != "Under Maintenance" and car.get("seating_capacity", "4") == seating_capacity:
            print(car["car_id"], "\t", car["model"], "\t", car["car_type"],
                  "\t", car.get("seating_capacity", "4"), "\tRs.", car["price_per_day"], "\t", car["status"])
            count = count + 1

    return count

def book_car(user):
    print("==============================")
    print("         BOOK A CAR")
    print("==============================")

    seating_capacity = choose_seating_capacity()

    if seating_capacity == "":
        return

    if print_bookable_cars(seating_capacity) == 0:
        print("No bookable cars match that seating capacity.")
        input("Press Enter to continue...")
        return

    print("Driver charge: Rs.", DRIVER_CHARGE_PER_DAY, "per day (only for 'With Driver').")
    car_id = input("Enter Car ID to book (or B to go back): ").strip()

    if car_id.lower() == "b":
        return

    car = find_record("cars", "car_id", car_id)

    if car == "":
        print("Car not found.")
        input("Press Enter to continue...")
        return

    if car.get("seating_capacity", "4") != seating_capacity:
        print("This car does not match the selected seating capacity.")
        input("Press Enter to continue...")
        return

    print("1. Self Drive")
    print("2. With Driver")
    choice = input("Rental type: ").strip()

    if choice == "1":
        rental_type = "Self Drive"
    elif choice == "2":
        rental_type = "With Driver"
    else:
        print("Invalid choice. Booking cancelled.")
        input("Press Enter to continue...")
        return

    start = ask_date("Start date")

    if start == "":
        return

    end = ask_date("End date")

    if end == "":
        return

    ok, message, driver_id = check_booking_request(car_id, start, end, rental_type)

    if not ok:
        print("Booking not possible:", message)
        input("Press Enter to continue...")
        return

    days = days_between(start, end)
    base, driver_charge, total = calculate_price(to_float(car["price_per_day"]), days, rental_type)

    print("------------- PRICE BREAKDOWN -------------")
    print("Car:", car["model"])
    print("Days:", days, "x", show_money(to_float(car["price_per_day"])), "=", show_money(base))

    if rental_type == "With Driver":
        print("Driver:", days, "x", show_money(DRIVER_CHARGE_PER_DAY), "=", show_money(driver_charge))

    print("TOTAL:", show_money(total))
    print("-------------------------------------------")

    if input("Confirm booking? (Y/N): ").strip().lower() == "y":
        ok, message = create_booking(user["customer_id"], car_id, start, end, rental_type)
        print(message)
    else:
        print("Booking not made.")

    input("Press Enter to continue...")


def my_bookings(user):
    print("==============================")
    print("        MY BOOKINGS")
    print("==============================")

    count = 0

    for b in read_table("bookings"):
        if b["customer_id"] == user["customer_id"]:
            print_booking_line(b)
            count = count + 1

    if count == 0:
        print("You have no bookings yet.")

    input("Press Enter to continue...")


def ask_my_booking(user, action):
    # Asks for a booking ID and returns the booking only if it belongs to this customer.
    booking_id = input("Enter Booking ID to " + action + " (or B to go back): ").strip()

    if booking_id.lower() == "b":
        return ""

    b = get_booking_for(booking_id, user["customer_id"])

    if b == "":
        print("Booking not found.")

    return b


def view_booking_details(user):
    b = ask_my_booking(user, "view")

    if b != "":
        print_booking_details(b)

    input("Press Enter to continue...")


def customer_cancel_booking(user):
    b = ask_my_booking(user, "cancel")

    if b != "":
        print_booking_details(b)

        if input("Cancel this booking? (Y/N): ").strip().lower() == "y":
            ok, message = cancel_booking(b["booking_id"], user["customer_id"])
            print(message)
        else:
            print("Cancellation aborted.")

    input("Press Enter to continue...")


def customer_pay_booking(user):
    b = ask_my_booking(user, "pay")

    if b != "":
        print_booking_details(b)

        if input("Pay " + show_money(to_float(b["total_amount"])) + " now? (Y/N): ").strip().lower() == "y":
            ok, message = pay_booking(b["booking_id"], user["customer_id"])
            print(message)
        else:
            print("Payment aborted.")

    input("Press Enter to continue...")


def customer_dashboard(user=""):
    if user == "":
        print("No customer is logged in.")
        return

    while True:
        print("==============================")
        print("     CUSTOMER DASHBOARD")
        print("==============================")

        print("1. View Available Cars")
        print("2. View Car Details")
        print("3. Book a Car")
        print("4. My Bookings")
        print("5. View Booking Details")
        print("6. Cancel a Booking")
        print("7. Pay for a Booking")
        print("8. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_available_cars()

        elif choice == "2":
            view_car_details()

        elif choice == "3":
            book_car(user)

        elif choice == "4":
            my_bookings(user)

        elif choice == "5":
            view_booking_details(user)

        elif choice == "6":
            customer_cancel_booking(user)

        elif choice == "7":
            customer_pay_booking(user)

        elif choice == "8":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")


def customer_signup():
    while True:
        print("------------------------------")
        print("      CUSTOMER SIGN UP")
        print("------------------------------")

        name = input("Name: ").strip()

        if name == "":
            print("Name cannot be empty.")
            continue

        username = input("Username: ").strip()

        if username == "":
            print("Username cannot be empty.")
            continue

        password = input("Password: ").strip()

        if password == "":
            print("Password cannot be empty.")
            continue

        phone = input("Phone: ").strip()

        if phone == "":
            print("Phone cannot be empty.")
            continue

        if not valid_phone(phone):
            print("Phone must be exactly 10 digits.")
            continue

        if username_in_use(username):
            print("Username already exists.")
            print("1. Try Again")
            print("2. Back")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                continue

            elif choice == "2":
                break

            else:
                print("Invalid choice.")
                break

        customer_id = generate_id("customers", "customer_id")

        record = {
            "customer_id": customer_id,
            "name": name,
            "username": username,
            "password": password,
            "phone": phone
        }

        if add_record("customers", record):
            print("Customer registration successful!")
            print("Your Customer ID is:", customer_id)
        else:
            print("Registration failed. Please try again later.")

        input("Press Enter to continue...")
        break
