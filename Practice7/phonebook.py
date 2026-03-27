import psycopg2
import csv
from config import params

def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            print("✅ Таблица готова.")

def import_from_csv(filename):
    query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;"
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader) 
                    for row in reader:
                        cur.execute(query, row)
        print(f"✅ Данные из {filename} загружены.")
    except FileNotFoundError:
        print("❌ Файл CSV не найден.")

def add_contact(name, phone):
    query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, phone))
            print(f"✅ Контакт {name} добавлен.")

def update_contact(name, new_phone):
    """Обновление номера по имени (требование задания)"""
    query = "UPDATE phonebook SET phone = %s WHERE name = %s;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_phone, name))
            print(f"✅ Контакт {name} обновлен.")

def find_contacts(search_term):
    query = "SELECT name, phone FROM phonebook WHERE name ILIKE %s OR phone LIKE %s;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (f'%{search_term}%', f'%{search_term}%'))
            return cur.fetchall()

def delete_contact(target):
    query = "DELETE FROM phonebook WHERE name = %s OR phone = %s;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (target, target))
            print(f"🗑️ Контакт {target} удален.")

def main_menu():
    create_table()
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Import from CSV")
        print("2. Add contact")
        print("3. Update contact")
        print("4. Find contact")
        print("5. Delete contact")
        print("0. Exit")
        
        choice = input("Select action: ")
        
        if choice == '1':
            import_from_csv('contacts.csv')
        elif choice == '2':
            n = input("Name: ")
            p = input("Phone: ")
            add_contact(n, p)
        elif choice == '3':
            n = input("Name to update: ")
            p = input("New phone: ")
            update_contact(n, p)
        elif choice == '4':
            s = input("Search for: ")
            results = find_contacts(s)
            for r in results: print(f"{r[0]}: {r[1]}")
        elif choice == '5':
            t = input("Name or Phone to delete: ")
            delete_contact(t)
        elif choice == '0':
            break

if __name__ == "__main__":
    main_menu()
