# assistant/__main__.py
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.assistant_client import create_thread, send_message_to_thread, read_thread_messages
from db import init_db
import sys
import logging
from db import init_db, list_threads



def main():
    logging.info("Start Application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ =="__main__":
    init_db()
    while True:
        action = input("要執行什麼操作？(create / list / send / read)：").strip()

        if action == "create":
            title = input("input chat theme...")
            category = input("input category theme...")
            thread_id = create_thread(title=title, category=category)
            print(f"建立成功！thread_id: {thread_id}")

        elif action == "list":
            list_threads()

        elif action == "send":
            thread_id = input("請輸入要傳送訊息的 thread_id：").strip()
            message = input("請輸入你的訊息：").strip()
            reply = send_message_to_thread(thread_id, message)
            print(f"Assistant 回覆：\n{reply}")

        elif action == "read":
            thread_id = input("請輸入要查閱的 thread_id：").strip()
            read_thread_messages(thread_id)

        else:
            print("不支援的操作")
