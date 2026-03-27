import psycopg2
import csv
from config import params  # Импортируем параметры из твоего config.py

def create_table():
    """Создает таблицу в базе данных, если её нет"""
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    );
    """
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                print("✅ База данных готова к работе.")
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")

def import_from_csv(filename):
    """Загружает данные из CSV файла"""
    query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;"
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Пропускаем заголовок (name, phone)
                    for row in reader:
                        cur.execute(query, row)
        print(f"✅ Данные из '{filename}' успешно импортированы.")
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден!")
    except Exception as e:
        print(f"❌ Ошибка при импорте: {e}")

def add_contact(name, phone):
    """Добавляет один контакт вручную"""
    query = "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, phone))
            print(f"✅ Контакт '{name}' добавлен.")

def update_contact(name, new_phone):
    """Обновляет номер телефона по имени"""
    query = "UPDATE phonebook SET phone = %s WHERE name = %s;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (new_phone, name))
            print(f"✅ Номер для '{name}' обновлен.")

def find_contacts(search_term):
    """Ищет контакты по имени или номеру"""
    query = "SELECT name, phone FROM phonebook WHERE name ILIKE %s OR phone LIKE %s;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (f'%{search_term}%', f'%{search_term}%'))
            return cur.fetchall()

def delete_contact(target):
    """Удаляет контакт по имени или номеру"""
    query = "DELETE FROM phonebook WHERE name = %s OR phone = %s;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (target, target))
            print(f"🗑️ Контакт '{target}' удален (если он был в базе).")

def get_all_contacts():
    """Выводит вообще все записи из базы"""
    query = "SELECT name, phone FROM phonebook ORDER BY name;"
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def main_menu():
    """Главное консольное меню"""
    create_table()
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Import from CSV")
        print("2. Add new contact")
        print("3. Update contact phone")
        print("4. Find contact (by name/phone)")
        print("5. Delete contact")
        print("6. Show ALL contacts")
        print("0. Exit")
        
        choice = input("\nSelect action: ")
        
        if choice == '1':
            import_from_csv('contacts.csv')
        
        elif choice == '2':
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            add_contact(name, phone)
            
        elif choice == '3':
            name = input("Enter name to update: ")
            new_phone = input("Enter new phone: ")
            update_contact(name, new_phone)
            
        elif choice == '4':
            s = input("Enter name or part of phone: ")
            results = find_contacts(s)
            if results:
                print(f"\nFound {len(results)} match(es):")
                for row in results:
                    print(f"👤 Name: {row[0]} | 📞 Phone: {row[1]}")
            else:
                print("❌ No matches found.")
                
        elif choice == '5':
            target = input("Enter name or phone to delete: ")
            delete_contact(target)
            
        elif choice == '6':
            all_data = get_all_contacts()
            if all_data:
                print("\n--- LIST OF ALL CONTACTS ---")
                for row in all_data:
                    print(f"👤 {row[0]}: {row[1]}")
            else:
                print("\nPhonebook is empty.")
                
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main_menu()