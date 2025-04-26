import psycopg2
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="Danko17100603"
)
cur = conn.cursor()

# 1. Insert from console
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("CALL insert_or_update_user(%s, %s)", (username, phone))
    conn.commit()
    print("User inserted/updated successfully.")

# 2. Insert from CSV
def insert_from_csv():
    path = input("Enter CSV file path: ")
    usernames = []
    phones = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            usernames.append(row[0])
            phones.append(row[1])
    cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))
    conn.commit()
    print("CSV data inserted successfully.")

# 3. Update data (manual)
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

# 4. Query data
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
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        rows = cur.fetchall()
    elif choice == '5':
        limit = int(input("Limit: "))
        offset = int(input("Offset: "))
        cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
    else:
        return

    for row in rows:
        print(row)

# 5. Delete data
def delete_data():
    value = input("Enter username or phone to delete: ")
    cur.execute("CALL delete_user(%s)", (value,))
    conn.commit()
    print("Deleted successfully.")

# 6. Insert many users from input
def insert_many_from_input():
    n = int(input("How many users to insert: "))
    usernames = []
    phones = []
    for _ in range(n):
        name = input("Username: ")
        phone = input("Phone: ")
        usernames.append(name)
        phones.append(phone)
    cur.execute("CALL insert_many_users(%s, %s)", (usernames, phones))
    conn.commit()
    print("Bulk insert completed.")

# 7. Menu loop
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
