import psycopg2
import json
from config import params

# --- Базовые операции ---

def add_contact_full(name, email, birthday, phone, phone_type, group_name):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            # 1. Сначала создаем сам контакт (или обновляем данные), если его нет
            cur.execute("""
                INSERT INTO contacts (name, email, birthday) 
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO UPDATE 
                SET email = EXCLUDED.email, birthday = EXCLUDED.birthday
            """, (name, email, birthday))
            
            # 2. Теперь привязываем к группе (создаст группу, если надо, и привяжет)
            cur.execute("CALL move_to_group(%s, %s)", (name, group_name))
            
            # 3. Теперь добавляем телефон (теперь контакт точно существует)
            cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
    print(f"Контакт {name} полностью добавлен!")

# --- Поиск и Фильтрация (Пункт 3.2) ---

def search_console():
    query = input("Введите запрос для поиска (имя, email или телефон): ")
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (query,))
            results = cur.fetchall()
            for r in results:
                print(f"👤 {r[0]} | Email: {r[1]} | Группа: {r[2]} | Номера: {r[3]}")

# --- Интерактивная Пагинация (Пункт 3.2) ---

def show_with_pagination(limit=5):
    offset = 0
    while True:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                # Используем твою функцию из Practice 8, адаптированную под новую схему
                cur.execute("""
                    SELECT name, email FROM contacts 
                    ORDER BY name LIMIT %s OFFSET %s
                """, (limit, offset))
                rows = cur.fetchall()
                
                print(f"\n--- Страница (offset: {offset}) ---")
                for row in rows:
                    print(f"- {row[0]} ({row[1]})")
                
                cmd = input("\n[n] Next, [p] Prev, [q] Quit: ").lower()
                if cmd == 'n': offset += limit
                elif cmd == 'p': offset = max(0, offset - limit)
                elif cmd == 'q': break

# --- Импорт / Экспорт (Пункт 3.3) ---

def export_to_json(filename="contacts.json"):
    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, c.email, c.birthday, g.name, 
                       string_agg(p.phone || ':' || p.type, ',') 
                FROM contacts c
                LEFT JOIN groups g ON c.group_id = g.id
                LEFT JOIN phones p ON c.id = p.contact_id
                GROUP BY c.id, g.name
            """)
            rows = cur.fetchall()
            data = [{"name": r[0], "email": r[1], "birthday": str(r[2]), "group": r[3], "phones": r[4].split(',') if r[4] else []} for r in rows]
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
    print(f"💾 Экспортировано в {filename}")

def import_from_json(filename="contacts.json"):
    with open(filename, "r") as f:
        data = json.load(f)
    for item in data:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM contacts WHERE name = %s", (item['name'],))
                if cur.fetchone():
                    if input(f"❓ {item['name']} уже есть. Перезаписать? (y/n): ").lower() != 'y': continue
                    cur.execute("DELETE FROM contacts WHERE name = %s", (item['name'],))
                p_info = item['phones'][0].split(':') if item['phones'] else ["None", "mobile"]
                add_contact_full(item['name'], item['email'], item['birthday'], p_info[0], p_info[1], item['group'])

# --- ГЛАВНОЕ МЕНЮ ---

if __name__ == "__main__":
    while True:
        print("\n--- PHONEBOOK TSIS 1 ---")
        print("1. Добавить контакт")
        print("2. Поиск (имя/email/тел)")
        print("3. Просмотр с пагинацией")
        print("4. Экспорт в JSON")
        print("5. Импорт из JSON")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == '1':
            name = input("Имя: ")
            email = input("Email: ")
            bday = input("Дата (YYYY-MM-DD): ")
            phone = input("Телефон: ")
            ptype = input("Тип (home/work/mobile): ")
            group = input("Группа: ")
            add_contact_full(name, email, bday, phone, ptype, group)
        elif choice == '2':
            search_console()
        elif choice == '3':
            show_with_pagination()
        elif choice == '4':
            export_to_json()
        elif choice == '5':
            import_from_json()
        elif choice == '0':
            break