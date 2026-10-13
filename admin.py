from database import add_record, delete_record, find_record, generate_id, read_table, update_record
from booking import car_has_active_booking

CAR_TYPES = ["Hatchback", "Sedan", "SUV", "MPV"]

def print_cars(cars):
    print("ID\tMODEL\t\tTYPE\t\tPRICE/DAY\tSTATUS")
    print("--------------------------------------------------------------")

    for car in cars:
        print(
            car["car_id"],
            "\t",
            car["model"],
            "\t",
            car["car_type"],
            "\t",
            "Rs.",
            car["price_per_day"],
            "\t",
            car["status"]
        )


def view_cars():
    print("==============================================================")
    print("                        CAR LIST")
    print("==============================================================")

    cars = read_table("cars")

    if not cars:
        print("No cars found.")
    else:
        print_cars(cars)

    input("Press Enter to continue...")


def choose_car_type():
    # Returns a car type from the fixed list, or "" if cancelled.
    for i in range(len(CAR_TYPES)):
        print(str(i + 1) + ".", CAR_TYPES[i])

    print(str(len(CAR_TYPES) + 1) + ". Cancel")
    choice = input("Choose car type: ").strip()

    for i in range(len(CAR_TYPES)):
        if choice == str(i + 1):
            return CAR_TYPES[i]

    return ""


def ask_price(prompt):
    # Returns a positive number, or 0 if the user types B.
    while True:
        text = input(prompt + " (or B to cancel): ").strip()

        if text.lower() == "b":
            return 0

        try:
            price = float(text)
        except ValueError:
            print("Enter a valid numeric price.")
            continue

        if price <= 0:
            print("Price must be greater than zero.")
        else:
            return price


def add_car():
    print("------------------------------")
    print("         ADD NEW CAR")
    print("------------------------------")

    model = input("Car Model: ").strip()

    if model == "":
        print("Model cannot be empty.")
        input("Press Enter to continue...")
        return

    car_type = choose_car_type()

    if car_type == "":
        print("Add car cancelled.")
        input("Press Enter to continue...")
        return

    price = ask_price("Price per Day")

    if price == 0:
        print("Add car cancelled.")
        input("Press Enter to continue...")
        return

    print("1. Available")
    print("2. Under Maintenance")
    print("3. Cancel")

    choice = input("Enter status: ").strip()

    if choice == "1":
        status = "Available"
    elif choice == "2":
        status = "Under Maintenance"
    else:
        print("Add car cancelled.")
        input("Press Enter to continue...")
        return

    car_id = generate_id("cars", "car_id")

    if add_record("cars", {
        "car_id": car_id,
        "model": model,
        "car_type": car_type,
        "price_per_day": price,
        "status": status
    }):
        print("Car added successfully!")
        print("Car ID:", car_id)
    else:
        print("Car could not be added.")

    input("Press Enter to continue...")


def update_car():
    print("------------------------------")
    print("         UPDATE CAR")
    print("------------------------------")

    cars = read_table("cars")

    if not cars:
        print("No cars available.")
        input("Press Enter to continue...")
        return

    print_cars(cars)

    while True:
        car_id = input("Enter Car ID to update (or B to go back): ").strip()

        if car_id.lower() == "b":
            return

        car = find_record("cars", "car_id", car_id)

        if car:
            break

        print("Car not found. Please enter a valid Car ID.")

    print("1. Model")
    print("2. Car Type")
    print("3. Price per Day")
    print("4. Status")
    print("5. Cancel")

    choice = input("Enter your choice: ").strip()
    changes = {}

    if choice == "1":
        value = input("Enter new model: ").strip()

        if value == "":
            print("Value cannot be empty.")
            input("Press Enter to continue...")
            return

        changes["model"] = value

    elif choice == "2":
        value = choose_car_type()

        if value == "":
            print("Update cancelled.")
            input("Press Enter to continue...")
            return

        changes["car_type"] = value

    elif choice == "3":
        if car_has_active_booking(car_id):
            print("This car has Booked/Ongoing rentals, so its price cannot be changed now.")
            input("Press Enter to continue...")
            return

        price = ask_price("Enter new price per day")

        if price == 0:
            print("Update cancelled.")
            input("Press Enter to continue...")
            return

        changes["price_per_day"] = price

    elif choice == "4":
        if car["status"] == "Rented":
            print("This car is currently rented. Complete the rental first.")
            input("Press Enter to continue...")
            return

        print("1. Available")
        print("2. Under Maintenance")

        status = input("Enter new status: ").strip()

        if status == "1":
            changes["status"] = "Available"
        elif status == "2":
            if car_has_active_booking(car_id):
                print("This car has Booked/Ongoing rentals and cannot go under maintenance.")
                input("Press Enter to continue...")
                return

            changes["status"] = "Under Maintenance"
        else:
            print("Invalid status.")
            input("Press Enter to continue...")
            return

    else:
        print("Update cancelled.")
        input("Press Enter to continue...")
        return

    if update_record("cars", "car_id", car_id, changes):
        print("Car updated successfully!")
    else:
        print("Car could not be updated.")

    input("Press Enter to continue...")


def delete_car():
    print("------------------------------")
    print("         DELETE CAR")
    print("------------------------------")

    cars = read_table("cars")

    if not cars:
        print("No cars available.")
        input("Press Enter to continue...")
        return

    print_cars(cars)

    car_id = input("Enter Car ID to delete (or B to go back): ").strip()

    if car_id.lower() == "b":
        return

    car = find_record("cars", "car_id", car_id)

    if not car:
        print("Car not found.")
        input("Press Enter to continue...")
        return

    if car["status"] == "Rented" or car_has_active_booking(car_id):
        print("This car has Booked/Ongoing rentals and cannot be deleted.")
        input("Press Enter to continue...")
        return

    print("Selected Car")
    print("Car ID:", car["car_id"])
    print("Model:", car["model"])
    print("Type:", car["car_type"])
    print("Price per Day:", car["price_per_day"])
    print("Status:", car["status"])

    confirmation = input("Delete this car? (Y/N): ").strip().lower()

    if confirmation == "y":
        if delete_record("cars", "car_id", car_id):
            print("Car deleted successfully!")
        else:
            print("Car could not be deleted.")
    else:
        print("Delete cancelled.")

    input("Press Enter to continue...")


def admin_dashboard(user=""):
    while True:
        print("==============================")
        print("        ADMIN DASHBOARD")
        print("==============================")

        print("1. View Cars")
        print("2. Add New Car")
        print("3. Update Car")
        print("4. Delete Car")
        print("5. Add Driver")
        print("6. View Users")
        print("7. Update Driver")
        print("8. Delete Driver")
        print("9. Manage Bookings")
        print("10. Reports")
        print("11. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_cars()

        elif choice == "2":
            add_car()

        elif choice == "3":
            update_car()

        elif choice == "4":
            delete_car()

        elif choice == "5":
            from admin_users import add_driver
            add_driver()

        elif choice == "6":
            from admin_users import view_users
            view_users()

        elif choice == "7":
            from admin_users import update_driver
            update_driver()

        elif choice == "8":
            from admin_users import delete_driver
            delete_driver()

        elif choice == "9":
            from admin_bookings import manage_bookings
            manage_bookings()

        elif choice == "10":
            from reports import reports_menu
            reports_menu()

        elif choice == "11":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")
