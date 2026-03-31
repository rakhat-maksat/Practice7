import csv
import psycopg2
from connect import get_connection

def insert_contacts(phonebook):
    conn = get_connection()
    if not conn:
        print("No DB connection")
        return

    cursor = conn.cursor()

    for person in phonebook:
        cursor.execute("""
            INSERT INTO contacts (first_name, last_name, phone, email)
            VALUES (%s, %s, %s, %s)
        """, (
            person['first_name'],
            person['last_name'],
            person['phone'],
            person['email']
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print("Data inserted into database successfully!")

def read_phonebook(filename):
    phonebook = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            clean_row = {key.strip(): value for key, value in row.items()}
            phonebook.append(clean_row)
    return phonebook


def display_phonebook(phonebook):
    for person in phonebook:
        print(f"Name: {person['first_name']} {person['last_name']}, Phone: {person['phone']}, Email: {person['email']}")


filename = "contacts.csv"
data = read_phonebook(filename)

display_phonebook(data)

insert_contacts(data)

conn = get_connection()

if conn:
    print("Connected successfully!")
    conn.close()
else:
    print("Connection failed")