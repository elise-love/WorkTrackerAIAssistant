#mem/log_writer.py

import sqlite3
from datetime import datetime

def log_message(profile_id: str, sender: str, content:str, category:str="chat"):
        conn = sqlite3.connect("conversation_log.db")
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat(timespec = "seconds")
        cursor.execute('''
            Insert INTO conversation_log (profile_id, sender, timestamp, content, category)
            VALUES (?,?,?,?,?)
        ''',(profile_id, sender, timestamp, content, category))

        conn.commit()
        conn.close()
