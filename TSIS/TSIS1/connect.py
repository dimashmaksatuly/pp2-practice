import psycopg2
from config import params

def test_connection():
    try:
        conn = psycopg2.connect(**params)
        print("Успешное подключение к tsis1_db!")
        conn.close()
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_connection()