#mem/conversation_log_db.py
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def create_db():
    try:
        conn= sqlite3.connect("conversation_log.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_log(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id TEXT,
                sender TEXT,
                timestamp TEXT,
                content TEXT,
                category TEXT
            )
        ''')

        conn.commit()

    except sqlite3.Error as e:
        logging.error(f"[資料庫錯誤] {e}")

    finally:
        if 'conn' in locals():
            conn.close()

def veiw_all_tables():
    try:
        conn = sqlite3.connect("conversation_log.db")
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        logging.info(f"目前資料庫中的資料表：")
        for table in tables:
            logging.info(f" -{table[0]}")

    except sqlite3.Error as e:
        logging.error(f"[資料庫錯誤] {e}")

    finally:
        if conn:
            conn.close

def veiw_all_logs():
    try:
        conn = sqlite3.connect("conversation_log.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM conversation_log")
        rows = cursor.fetchall()

        logging.info("目前所有對話紀錄如下：")
        for row in rows:
            logging.info(row)

    except sqlite3.Error as e:
        logging.error(f"[資料庫錯誤] {e}")

    finally:
        if conn:
            conn.close

veiw_all_tables()
veiw_all_logs()

if __name__ == '__main__':
    create_db()