# Driver dashboard: a driver sees and changes only their own assignments.

from database import find_record, update_record
from database import read_table
from booking import print_booking_line, print_booking_details, get_booking_for
from booking import start_rental, return_rental, driver_has_active_booking
from dates import ask_date


def view_my_assignments(user):
    print("==============================")
    print("       MY ASSIGNMENTS")
    print("==============================")

    count = 0

    for b in read_table("bookings"):
        if b["driver_id"] == user["driver_id"]:
            print_booking_line(b)
            count = count + 1

    if count == 0:
        print("You have no assignments.")

    input("Press Enter to continue...")


def ask_my_assignment(user, action):
    booking_id = input("Enter Booking ID to " + action + " (or B to go back): ").strip()

    if booking_id.lower() == "b":
        return ""

    b = get_booking_for(booking_id, "", user["driver_id"])

    if b == "":
        print("Assignment not found.")

    return b


def view_assignment_details(user):
    b = ask_my_assignment(user, "view")

    if b != "":
        print_booking_details(b, True)

    input("Press Enter to continue...")


def driver_start_rental(user):
    b = ask_my_assignment(user, "start")

    if b != "":
        print_booking_details(b, True)
        ok, message = start_rental(b["booking_id"], user["driver_id"])
        print(message)

    input("Press Enter to continue...")


def driver_return_rental(user):
    b = ask_my_assignment(user, "complete")

    if b != "":
        print_booking_details(b, True)
        return_date = ask_date("Actual return date")

        if return_date != "":
            ok, message = return_rental(b["booking_id"], return_date, user["driver_id"])
            print(message)

    input("Press Enter to continue...")


def set_my_availability(user):
    me = find_record("drivers", "driver_id", user["driver_id"])

    if me == "":
        print("Driver record not found.")
        input("Press Enter to continue...")
        return

    print("Current availability:", me["availability"])
    print("1. Available")
    print("2. Offline")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        new_value = "Available"
    elif choice == "2":
        new_value = "Offline"

        if driver_has_active_booking(user["driver_id"]):
            print("You have Booked/Ongoing assignments, so you cannot go Offline.")
            input("Press Enter to continue...")
            return
    else:
        print("Invalid choice.")
        input("Press Enter to continue...")
        return

    if update_record("drivers", "driver_id", user["driver_id"], {"availability": new_value}):
        print("Availability updated.")
    else:
        print("Could not update availability.")

    input("Press Enter to continue...")


def driver_dashboard(user=""):
    if user == "":
        print("No driver is logged in.")
        return

    while True:
        print("==============================")
        print("      DRIVER DASHBOARD")
        print("==============================")

        print("1. View My Assignments")
        print("2. View Assignment Details")
        print("3. Start Rental")
        print("4. Complete Rental (Return)")
        print("5. Set My Availability")
        print("6. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_my_assignments(user)

        elif choice == "2":
            view_assignment_details(user)

        elif choice == "3":
            driver_start_rental(user)

        elif choice == "4":
            driver_return_rental(user)

        elif choice == "5":
            set_my_availability(user)

        elif choice == "6":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please try again.")
