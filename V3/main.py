1

from login import login, customer_menu
from database import create_missing_files


def profile_selection():
    while True:
        print("==============================")
        print("      CAR RENTAL SYSTEM")
        print("==============================")

        print("1. Administrator")
        print("2. Driver")
        print("3. Customer")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            login("Administrator")

        elif choice == "2":
            login("Driver")

        elif choice == "3":
            customer_menu()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")


create_missing_files()

try:
    profile_selection()
except EOFError:
    print("Input ended. Exiting...")
