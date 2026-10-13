
from database import find_by_username


def login(profile):
    table_map = {
        "Administrator": "administrators",
        "Driver": "drivers",
        "Customer": "customers"
    }

    if profile not in table_map:
        print("Invalid profile.")
        return

    table = table_map[profile]

    while True:
        print("------------------------------")
        print(profile + " LOGIN")
        print("------------------------------")

        username = input("Username: ").strip()

        if username == "":
            print("Username cannot be empty.")
            continue

        password = input("Password: ").strip()

        if password == "":
            print("Password cannot be empty.")
            continue

        result = find_by_username(table, username)

        if result != "" and result.get("password", "") == password:
            print("Login successful!")
            print("Welcome", result.get("name", ""))

            if profile == "Administrator":
                from admin import admin_dashboard
                admin_dashboard(result)

            elif profile == "Driver":
                from driver import driver_dashboard
                driver_dashboard(result)

            elif profile == "Customer":
                from customer import customer_dashboard
                customer_dashboard(result)

            break

        print("Invalid username or password.")
        print("1. Try Again")
        print("2. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "2":
            break

        elif choice == "1":
            continue

        else:
            print("Invalid choice. Please enter 1 or 2.")


def customer_menu():
    while True:
        print("------------------------------")
        print("       CUSTOMER MENU")
        print("------------------------------")
        print("1. Login")
        print("2. Sign Up")
        print("3. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            login("Customer")

        elif choice == "2":
            from customer import customer_signup
            customer_signup()

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")
