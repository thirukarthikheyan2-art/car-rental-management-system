
import csv
import os

TABLE_FILES = {
    "administrators": "administrators.csv",
    "drivers": "drivers.csv",
    "customers": "customers.csv",
    "cars": "cars.csv",
    "bookings": "bookings.csv"
}


HEADERS = {
    "administrators": ["admin_id", "name", "username", "password", "phone"],
    "drivers": ["driver_id", "name", "username", "password", "phone", "availability"],
    "customers": ["customer_id", "name", "username", "password", "phone"],
    "cars": ["car_id", "model", "car_type", "price_per_day", "status"],
    "bookings": [
        "booking_id",
        "customer_id",
        "car_id",
        "start_date",
        "end_date",
        "rental_type",
        "driver_id",
        "total_amount",
        "status",
        "payment_status"
    ]

}


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_path(table):
    if table in TABLE_FILES:
        return os.path.join(PROJECT_DIR, TABLE_FILES[table])

    return ""


def read_table(table):
    rows = []

    if table not in TABLE_FILES:
        return rows

    p = get_path(table)

    try:
        f = open(p, "r", newline="")
        r = csv.reader(f)
        first = True

        for i in r:
            if first:
                first = False

                if i != HEADERS[table]:
                    f.close()
                    print("Invalid CSV header in", p)
                    return rows

                continue

            if len(i) == len(HEADERS[table]):
                row = {}

                for j in range(len(HEADERS[table])):
                    row[HEADERS[table][j]] = i[j]

                rows.append(row)

        f.close()

    except FileNotFoundError:
        print("File not found:", p)

    return rows


def table_ready(table):
    # True only if the CSV file exists and has the correct header.
    if table not in TABLE_FILES:
        return False

    try:
        f = open(get_path(table), "r", newline="")
        r = csv.reader(f)
        first = []

        for i in r:
            first = i
            break

        f.close()
        return first == HEADERS[table]

    except OSError:
        return False


def create_missing_files():
    # Creates any missing CSV file with its header row. Existing files are never touched.
    for table in TABLE_FILES:
        try:
            f = open(get_path(table), "r", newline="")
            f.close()
        except FileNotFoundError:
            try:
                f = open(get_path(table), "w", newline="")
                w = csv.writer(f)
                w.writerow(HEADERS[table])
                f.close()
            except OSError:
                print("Could not create", get_path(table))


def write_table(table, rows):
    if table not in TABLE_FILES:
        return False

    p = get_path(table)

    try:
        f = open(p, "w", newline="")
        w = csv.writer(f)

        w.writerow(HEADERS[table])

        for i in rows:
            row = []

            for j in HEADERS[table]:
                row.append(i.get(j, ""))

            w.writerow(row)

        f.close()
        return True

    except OSError:
        print("Could not write to", p, "- is the file open in another program?")
        return False


def add_record(table, record):
    if table not in TABLE_FILES:
        return False

    if not table_ready(table):
        print("Cannot save:", get_path(table), "is missing or has an invalid header.")
        return False

    rows = read_table(table)
    row = {}

    for i in HEADERS[table]:
        row[i] = str(record.get(i, ""))

    rows.append(row)
    return write_table(table, rows)


def update_record(table, key_field, key_value, changes):
    if table not in TABLE_FILES:
        return False

    if key_field not in HEADERS[table]:
        return False

    if not table_ready(table):
        return False

    rows = read_table(table)

    for i in rows:
        if str(i.get(key_field, "")) == str(key_value):
            for j in changes:
                if j in HEADERS[table]:
                    i[j] = str(changes[j])

            return write_table(table, rows)

    return False


def delete_record(table, key_field, key_value):
    if table not in TABLE_FILES:
        return False

    if key_field not in HEADERS[table]:
        return False

    if not table_ready(table):
        return False

    rows = read_table(table)
    new_rows = []

    for i in rows:
        if str(i.get(key_field, "")) != str(key_value):
            new_rows.append(i)

    if len(new_rows) == len(rows):
        return False

    return write_table(table, new_rows)


def find_record(table, key_field, key_value):
    if table not in TABLE_FILES:
        return ""

    if key_field not in HEADERS[table]:
        return ""

    rows = read_table(table)

    for i in rows:
        if str(i.get(key_field, "")) == str(key_value):
            return i

    return ""


def find_by_username(table, username):
    if table not in TABLE_FILES:
        return ""

    if "username" not in HEADERS[table]:
        return ""

    rows = read_table(table)

    for i in rows:
        if i.get("username", "").lower() == username.lower():
            return i

    return ""


def generate_id(table, field):
    if table not in TABLE_FILES:
        return "1"

    if field not in HEADERS[table]:
        return "1"

    rows = read_table(table)
    n = 0

    for i in rows:
        try:
            x = int(i.get(field, 0))

            if x > n:
                n = x

        except ValueError:
            pass

    return str(n + 1)


ID_FIELDS = {
    "administrators": "admin_id",
    "drivers": "driver_id",
    "customers": "customer_id"
}


def username_in_use(username, own_table="", own_id=""):
    # True if the username (any capitals) exists in ANY user table.
    # own_table / own_id let a record keep its own username when it is edited.
    for table in ID_FIELDS:
        record = find_by_username(table, username)

        if record != "":
            if table == own_table and record[ID_FIELDS[table]] == own_id:
                continue

            return True

    return False


def valid_phone(phone):
    if len(phone) != 10:
        return False

    for ch in phone:
        if ch not in "0123456789":
            return False

    return True
