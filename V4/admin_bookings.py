# Administrator booking management.

from database import read_table
from booking import print_booking_line, print_booking_details, get_booking_for
from booking import start_rental, return_rental, cancel_booking
from dates import ask_date


def view_all_bookings():
    print("==============================")
    print("         ALL BOOKINGS")
    print("==============================")

    bookings = read_table("bookings")

    if len(bookings) == 0:
        print("No bookings found.")

    if len(bookings) > 0:
        print("{:<12} {:<22} {:<23} {:<13} {:>12} {:<12} {:<14}".format(
            "BOOKING ID", "CAR", "DATES", "RENTAL TYPE", "TOTAL", "STATUS", "PAYMENT"))
        print("-" * 112)

    for b in bookings:
        print_booking_line(b)

    input("Press Enter to continue...")


def ask_booking(action):
    booking_id = input("Enter Booking ID to " + action + " (or B to go back): ").strip()

    if booking_id.lower() == "b":
        return ""

    b = get_booking_for(booking_id)

    if b == "":
        print("Booking not found.")

    return b


def admin_start_rental():
    b = ask_booking("start")

    if b != "":
        print_booking_details(b, True)
        ok, message = start_rental(b["booking_id"])
        print(message)

    input("Press Enter to continue...")


def admin_return_rental():
    b = ask_booking("return")

    if b != "":
        print_booking_details(b, True)
        return_date = ask_date("Actual return date")

        if return_date != "":
            ok, message = return_rental(b["booking_id"], return_date)
            print(message)

    input("Press Enter to continue...")


def admin_cancel_booking():
    b = ask_booking("cancel")

    if b != "":
        print_booking_details(b, True)

        if input("Cancel this booking? (Y/N): ").strip().lower() == "y":
            ok, message = cancel_booking(b["booking_id"])
            print(message)
        else:
            print("Cancellation aborted.")

    input("Press Enter to continue...")


def manage_bookings():
    while True:
        print("==============================")
        print("       MANAGE BOOKINGS")
        print("==============================")
        print("1. View All Bookings")
        print("2. View Booking Details")
        print("3. Start Rental")
        print("4. Process Return")
        print("5. Cancel Booking")
        print("6. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_bookings()

        elif choice == "2":
            b = ask_booking("view")

            if b != "":
                print_booking_details(b, True)

            input("Press Enter to continue...")

        elif choice == "3":
            admin_start_rental()

        elif choice == "4":
            admin_return_rental()

        elif choice == "5":
            admin_cancel_booking()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")
