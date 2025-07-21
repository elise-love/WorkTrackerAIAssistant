#db.py
import sqlite3
import logging

DB_PATH = "assistant_threads.db"

logging.basicConfig(
    level=logging.ERROR,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)


def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threads (
                id TEXT PRIMARY KEY,
                assistant_id TEXT,
                title TEXT,
                category TEXT,
                created_at TEXT,
                token_usage INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        logging.debug(f"Database initialized.")

def list_threads():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
           SELECT id, title, category, token_usage
           FROM threads
           ORDER BY created_at DESC
        ''')
        return cursor.fetchall()  #只回傳資料


def get_thread_title_by_id(thread_id: str)->str:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM threads WHERE id = ?",(thread_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return "Unknown"

def get_thread_id_by_title(thread_title: str)->str:
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM threads WHERE title = ?",(thread_title))
        result = cursor.fetchone()
        if result:
            return result[0]
        return "Unknown"

if __name__ == "__main__":
    init_db()
    list_threads()
