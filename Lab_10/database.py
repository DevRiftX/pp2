import psycopg2
import csv

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="adasd"
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

# 2. Insert from console
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Inserted successfully.")

# 3. Insert from CSV
def insert_from_csv():
    path = input("Enter CSV file path: ")
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            username, phone = row
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
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
    print("Query options: (1) All, (2) By Username, (3) By Phone")
    choice = input("Select: ")
    if choice == '1':
        cur.execute("SELECT * FROM phonebook")
    elif choice == '2':
        name = input("Username: ")
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (name,))
    elif choice == '3':
        phone = input("Phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    else:
        return

    rows = cur.fetchall()
    for row in rows:
        print(row)

# 6. Delete data
def delete_data():
    print("Delete by: (1) Username, (2) Phone")
    choice = input("Select: ")
    if choice == '1':
        name = input("Username to delete: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (name,))
    elif choice == '2':
        phone = input("Phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    print("Deleted successfully.")

# 7. Menu loop
def main():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete data")
        print("6. Exit")
        option = input("Choose an option (1-6): ")

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
            break
        else:
            print("Invalid option.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()