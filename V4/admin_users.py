
from database import add_record, find_record, username_in_use, valid_phone
from booking import driver_has_active_booking
from database import generate_id, read_table, update_record, delete_record


def add_driver():
    print("------------------------------")
    print("         ADD DRIVER")
    print("------------------------------")

    name = input("Driver Name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    phone = input("Phone: ").strip()

    if name == "" or username == "" or password == "" or phone == "":
        print("All fields are required.")
        input("Press Enter to continue...")
        return

    if username_in_use(username):
        print("Username already exists.")
        input("Press Enter to continue...")
        return

    if not valid_phone(phone):
        print("Phone must be exactly 10 digits.")
        input("Press Enter to continue...")
        return

    print("1. Available")
    print("2. Offline")
    print("3. Cancel")

    choice = input("Enter availability: ").strip()

    if choice == "1":
        availability = "Available"
    elif choice == "2":
        availability = "Offline"
    elif choice == "3":
        print("Operation cancelled.")
        return
    else:
        print("Invalid choice.")
        return

    driver_id = generate_id("drivers", "driver_id")

    record = {
        "driver_id": driver_id,
        "name": name,
        "username": username,
        "password": password,
        "phone": phone,
        "availability": availability
    }

    if add_record("drivers", record):
        print("Driver added successfully!")
        print("Driver ID:", driver_id)
    else:
        print("Driver could not be added.")
    input("Press Enter to continue...")


def update_driver():
    print("------------------------------")
    print("        UPDATE DRIVER")
    print("------------------------------")

    drivers = read_table("drivers")

    if len(drivers) == 0:
        print("No drivers found.")
        input("Press Enter to continue...")
        return

    print("{:<10} {:<22} {:<20} {:<14} {:<14}".format(
        "ID", "NAME", "USERNAME", "PHONE", "STATUS"))
    print("-" * 82)

    for i in drivers:
        print("{:<10} {:<22} {:<20} {:<14} {:<14}".format(
            i["driver_id"], i["name"], i["username"], i["phone"], i["availability"]))

    driver_id = input("Enter Driver ID (or B to go back): ").strip()

    if driver_id.lower() == "b":
        return

    driver = find_record("drivers", "driver_id", driver_id)

    if driver == "":
        print("Driver not found.")
        input("Press Enter to continue...")
        return

    print("1. Update Name")
    print("2. Update Username")
    print("3. Update Password")
    print("4. Update Phone")
    print("5. Update Availability")
    print("6. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        value = input("Enter new name: ").strip()

        if value == "":
            print("Name cannot be empty.")
            return

        changes = {"name": value}

    elif choice == "2":
        value = input("Enter new username: ").strip()

        if value == "":
            print("Username cannot be empty.")
            return

        if username_in_use(value, "drivers", driver_id):
            print("Username already exists.")
            return

        changes = {"username": value}

    elif choice == "3":
        value = input("Enter new password: ").strip()

        if value == "":
            print("Password cannot be empty.")
            return

        changes = {"password": value}

    elif choice == "4":
        value = input("Enter new phone: ").strip()

        if not valid_phone(value):
            print("Phone must be exactly 10 digits.")
            return

        changes = {"phone": value}

    elif choice == "5":
        print("1. Available")
        print("2. Offline")

        value = input("Enter availability: ").strip()

        if value == "1":
            changes = {"availability": "Available"}
        elif value == "2":
            if driver_has_active_booking(driver_id):
                print("This driver has Booked/Ongoing assignments and cannot be set Offline.")
                input("Press Enter to continue...")
                return

            changes = {"availability": "Offline"}
        else:
            print("Invalid availability.")
            return

    elif choice == "6":
        print("Update cancelled.")
        return

    else:
        print("Invalid choice.")
        return

    if update_record("drivers", "driver_id", driver_id, changes):
        print("Driver updated successfully!")
    else:
        print("Driver could not be updated.")

    input("Press Enter to continue...")


def delete_driver():
    print("------------------------------")
    print("        DELETE DRIVER")
    print("------------------------------")

    drivers = read_table("drivers")

    if len(drivers) == 0:
        print("No drivers found.")
        input("Press Enter to continue...")
        return

    print("{:<10} {:<22} {:<20} {:<14}".format(
        "ID", "NAME", "USERNAME", "PHONE"))
    print("-" * 68)

    for i in drivers:
        print("{:<10} {:<22} {:<20} {:<14}".format(
            i["driver_id"], i["name"], i["username"], i["phone"]))

    driver_id = input("Enter Driver ID (or B to go back): ").strip()

    if driver_id.lower() == "b":
        return

    driver = find_record("drivers", "driver_id", driver_id)

    if driver == "":
        print("Driver not found.")
        input("Press Enter to continue...")
        return

    if driver_has_active_booking(driver_id):
        print("This driver has Booked/Ongoing assignments and cannot be deleted.")
        input("Press Enter to continue...")
        return

    print("Selected Driver:", driver["name"])
    confirmation = input("Delete this driver? (Y/N): ").strip().lower()

    if confirmation == "y":
        if delete_record("drivers", "driver_id", driver_id):
            print("Driver deleted successfully!")
        else:
            print("Driver could not be deleted.")
    else:
        print("Deletion cancelled.")

    input("Press Enter to continue...")


def view_users():
    print("------------------------------")
    print("         VIEW USERS")
    print("------------------------------")

    print("========== ADMINISTRATORS ==========")
    print("{:<10} {:<22} {:<20} {:<14}".format(
        "ID", "NAME", "USERNAME", "PHONE"))
    print("-" * 68)

    admins = read_table("administrators")

    if len(admins) == 0:
        print("No administrators found.")

    for admin in admins:
        print("{:<10} {:<22} {:<20} {:<14}".format(
            admin["admin_id"], admin["name"], admin["username"], admin["phone"]))

    print("============== DRIVERS =============")
    print("{:<10} {:<22} {:<20} {:<14} {:<14}".format(
        "ID", "NAME", "USERNAME", "PHONE", "STATUS"))
    print("-" * 82)

    drivers = read_table("drivers")

    if len(drivers) == 0:
        print("No drivers found.")

    for driver in drivers:
        print("{:<10} {:<22} {:<20} {:<14} {:<14}".format(
            driver["driver_id"], driver["name"], driver["username"],
            driver["phone"], driver["availability"]))

    print("============= CUSTOMERS =============")
    print("{:<10} {:<22} {:<20} {:<14}".format(
        "ID", "NAME", "USERNAME", "PHONE"))
    print("-" * 68)

    customers = read_table("customers")

    if len(customers) == 0:
        print("No customers found.")

    for customer in customers:
        print("{:<10} {:<22} {:<20} {:<14}".format(
            customer["customer_id"], customer["name"],
            customer["username"], customer["phone"]))

    input("Press Enter to continue...")
