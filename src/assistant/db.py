import sqlite3

DB_PATH = "assistant_threads.db"

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
        print("Database initialized.")

def list_threads():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
           SELECT id, title, category, created_at, token_usage
           FROM threads 
           ORDER BY created_at DESC       
        ''')
        rows = cursor.fetchall()
        print("\nThread List:")
        for row in rows:
            created_time = row[3][:19]
            thread_title = row[1] or "(Untitled)"
            thread_category = row[2] or "(Uncategorized)"
            token_usage = row[4]
            print(f"- [{created_time}]\n{thread_title} | 分類: {thread_category}\n Tokens:{token_usage}\n -> thread_id: {row[0]}\n")

if __name__ == "__main__":
    init_db()
    list_threads()
