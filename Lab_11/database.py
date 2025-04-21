import psycopg2
import csv, re

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="idk"
)
cur = conn.cursor()

# 1. Design table for PhoneBook
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
""")
conn.commit()

# --- Function 1: Search by pattern ---
def search_by_pattern(pattern):
    pattern = f"%{pattern}%"
    cur.execute("""
        SELECT * FROM phonebook
        WHERE username ILIKE %s OR phone ILIKE %s
    """, (pattern, pattern))
    return cur.fetchall()

# --- Procedure 2: Insert or update user ---
def insert_or_update_user(username, phone):
    cur.execute("SELECT * FROM phonebook WHERE username = %s", (username,))
    result = cur.fetchone()
    if result:
        cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (phone, username))
        print("User exists. Phone updated.")
    else:
        cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
        print("New user inserted.")
    conn.commit()

# --- Procedure 3: Insert many users with validation ---
def insert_many_users(user_list):
    incorrect_data = []
    for user in user_list:
        name, phone = user
        if not re.fullmatch(r"\+\d{10,15}", phone):
            incorrect_data.append(user)
            continue
        insert_or_update_user(name, phone)
    return incorrect_data

# --- Function 4: Query with pagination ---
def query_with_pagination(limit, offset):
    cur.execute("SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
    return cur.fetchall()

# --- Procedure 5: Delete by username or phone ---
def delete_by_username_or_phone(value):
    cur.execute("DELETE FROM phonebook WHERE username = %s OR phone = %s", (value, value))
    conn.commit()
    print("Deleted if matched.")

# 2. Insert from console
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    insert_or_update_user(username, phone)

# 3. Insert from CSV
def insert_from_csv():
    path = input("Enter CSV file path: ")
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            username, phone = row
            insert_or_update_user(username, phone)
    print("CSV data inserted successfully.")

# 4. Update data
def update_data():
    print("Update options: (1) Username, (2) Phone")
    choice = input("Select: ")
    if choice == '1':
        old_name = input("Old username: ")
        new_name = input("New username: ")
        cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_name, old_name))
    elif choice == '2':
        old_phone = input("Old phone: ")
        new_phone = input("New phone: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, old_phone))
    conn.commit()
    print("Updated successfully.")

# 5. Query data
def query_data():
    print("Query options: (1) All, (2) By Username, (3) By Phone, (4) By Pattern, (5) Paginated")
    choice = input("Select: ")
    if choice == '1':
        cur.execute("SELECT * FROM phonebook")
        rows = cur.fetchall()
    elif choice == '2':
        name = input("Username: ")
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (name,))
        rows = cur.fetchall()
    elif choice == '3':
        phone = input("Phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
        rows = cur.fetchall()
    elif choice == '4':
        pattern = input("Enter pattern: ")
        rows = search_by_pattern(pattern)
    elif choice == '5':
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        rows = query_with_pagination(limit, offset)
    else:
        return

    for row in rows:
        print(row)

# 6. Delete data
def delete_data():
    print("Delete by: (1) Username, (2) Phone, (3) Either")
    choice = input("Select: ")
    if choice == '1':
        name = input("Username to delete: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (name,))
    elif choice == '2':
        phone = input("Phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    elif choice == '3':
        value = input("Enter username or phone: ")
        delete_by_username_or_phone(value)
        return
    conn.commit()
    print("Deleted successfully.")

# 7. Insert many from list
def insert_many_from_input():
    n = int(input("How many users to insert: "))
    user_list = []
    for _ in range(n):
        name = input("Username: ")
        phone = input("Phone: ")
        user_list.append((name, phone))
    invalids = insert_many_users(user_list)
    if invalids:
        print("Invalid entries:", invalids)

# 8. Menu loop
def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("6. Insert many users with check")
        print("7. Exit")
        option = input("Choose an option (1-7): ")

        if option == '1':
            insert_from_console()
        elif option == '2':
            insert_from_csv()
        elif option == '3':
            update_data()
        elif option == '4':
            query_data()
        elif option == '5':
            delete_data()
        elif option == '6':
            insert_many_from_input()
        elif option == '7':
            break
        else:
            print("Invalid option.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()