import sqlite3

DB_PATH = "assistant_threads.db"

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threads(
                id TEXT PRIMARY KEY,
                assistant_id TEXT,
                title TEXT,
                category TEXT,
                created_at TEXT,
                token_usage INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def list_threads():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
           SELECT id, title, category, created_at
           FROM threads 
           ORDER BY created_at DESC       
        ''')
        rows = cursor.fetchall()
        print("\n Thread lists:")
        for row in rows:
            print(f"-[{row[3][:19]}]\n{row[1]}|\n分類:{[row]}\n -> thread_id:{row[0]}")

if __name__ == "__main__":
    init_db()