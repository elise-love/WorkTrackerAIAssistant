# assistant/__main__.py
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.assistant_client import create_thread, send_message_to_thread, read_thread_messages
from db import init_db
import sys
import logging
from db import init_db, list_threads

logging.basicConfig(
    level=logging.ERROR,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)


def main():
    logging.info("Start Application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ =="__main__":
    init_db()
    current_thread = "thread_gWYQtMUDzCaOVevawWBHTjwe"
    while True:
        if current_thread == "thread_gWYQtMUDzCaOVevawWBHTjwe":
            print("Current Thread: Chat 1")
        elif current_thread == "thread_ZeDc9lBLx03HWPSP2tnsQxZH":
            print("Current Thread: daily_planning")

        elif current_thread == "thread_W0wQgMj82xp7btUWMg8Zuy5f":
            print("Current Thread: life_talk")

        else:
            print("Current Thread: TestChatTheme1")

        print("(type \ for instrunction)\n")

        message = input("芍芍: ").strip()

        if message == "\\":
            action = input("Input number for instructions\n1: Change Thread\n2: List Threads\n3: Read Threat History\n4: Create Thread\n\nExecute: ")
            print()

            if action == "1":
                new_thread_choice = input("Choose Thread:\n1: Chat1\n2: daily_planning\n3: life_talk\n4: TestChatTheme1\n\nExecute: ")
                print()
                if new_thread_choice =="1":
                    current_thread = "thread_viYMHiRdWbF1uKul2pimdq2T"
                elif new_thread_choice =="2":
                    current_thread = "thread_ZeDc9lBLx03HWPSP2tnsQxZH"
                elif new_thread_choice =="3":
                    current_thread = "thread_W0wQgMj82xp7btUWMg8Zuy5f"
                elif new_thread_choice =="4":
                    current_thread = "thread_gWYQtMUDzCaOVevawWBHTjwe"
                else:
                    print("不支援的操作")
                continue

            elif action == "2":
                list_threads()

            elif action == "3":
                read_thread = input("Read Thread:\n1: Chat1\n2: daily_planning\n3: life_talk\n4: TestChatTheme1\n\nExecute: ").strip()
                if read_thread =="1":
                    read_thread_id = "thread_viYMHiRdWbF1uKul2pimdq2T"
                elif read_thread =="2":
                    read_thread_id = "thread_ZeDc9lBLx03HWPSP2tnsQxZH"
                elif read_thread =="3":
                    read_thread_id = "thread_W0wQgMj82xp7btUWMg8Zuy5f"
                elif read_thread =="4":
                    read_thread_id = "thread_gWYQtMUDzCaOVevawWBHTjwe"
                else:
                    print("不支援的操作")
                print()
                read_thread_messages(read_thread_id)

            elif action == "4":
            i    title = input("input chat theme...")
                category = input("input category theme...")
                thread_id = create_thread(title=title, category=category)
                print(f"建立成功！thread_id: {thread_id}")

            else:
                print("不支援的操作")

        else:
            reply = send_message_to_thread(current_thread, message)
            print("-------------------------------------------------------------------------------------------------------")
            print(f"精靈：\n{reply}")
            print("-------------------------------------------------------------------------------------------------------")


      