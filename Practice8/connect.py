import psycopg2
from config import params

def test_connection():
    try:
        conn = psycopg2.connect(**params)
        print("Connected successfully to phonebook_db!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()