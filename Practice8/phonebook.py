import psycopg2
from config import params

def add_or_update(name, phone):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    print(f"Done upsert for: {name}")

def find_contacts(pattern):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            return cur.fetchall()

def insert_many(names, phones):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))
    print("Bulk insert process finished.")

def get_page(limit, offset):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            return cur.fetchall()

def remove_contact(target):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s)", (target,))
    print(f"Removed: {target}")

if __name__ == "__main__":
    # 1. Тест вставки/обновления
    add_or_update("Dimash", "77071112233")
    
    # 2. Тест поиска
    print("Search Result:", find_contacts("Dim"))
    
    # 3. Тест массовой вставки
    names_list = ["Alice", "Bob", "Charlie"]
    phones_list = ["7015554433", "7026665544", "123"] 
    insert_many(names_list, phones_list)
    
    # 4. Тест пагинации 
    print("Page 1:", get_page(2, 0))
    
    # 5. Тест удаления
    remove_contact("Alice")