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
        rows = cursor.fetchall()
        print("\nThread List:\n")
        for row in rows:
            thread_title = row[1] or "(Untitled)"
            thread_category = row[2] or "(Uncategorized)"
            token_usage = row[3]
            print(f"{thread_title}\n分類: {thread_category}\nTokens:{token_usage}\nthread_id: {row[0]}\n")

if __name__ == "__main__":
    init_db()
    list_threads()
