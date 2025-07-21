#type_window.py

from hmac import new
from PyQt5.QtWidgets import QWidget, QLabel,QVBoxLayout, QApplication, QTextEdit, QPlainTextEdit, QPushButton, QComboBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
import sys
import os
import logging
from core.assistant_client import send, read_thread_messages, create_thread
from db import list_threads, get_thread_title_by_id, get_thread_id_by_title

THREAD_NAME_ID_MAP = {
   "Chat1": "thread_viYMHiRdWbF1uKul2pimdq2T",
   "daily_planning": "thread_ZeDc9lBLx03HWPSP2tnsQxZH",
   "life_talk": "thread_W0wQgMj82xp7btUWMg8Zuy5f",
   "TestChatTheme1": "thread_gWYQtMUDzCaOVevawWBHTjwe"       
}
THREAD_NUM_ID_MAP = {
   "1": "thread_viYMHiRdWbF1uKul2pimdq2T",
   "2": "thread_ZeDc9lBLx03HWPSP2tnsQxZH",
   "3": "thread_W0wQgMj82xp7btUWMg8Zuy5f",
   "4": "thread_gWYQtMUDzCaOVevawWBHTjwe"       
}
logging.basicConfig(
    level = logging.INFO,
    format = '[%(astime)s [%(levelname)s] %(message)s',
    handler = [logging.StreamHandler()]
)

class TypeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(800,600)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        #load background img
        current_dir = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(current_dir, "components", "type_window.png")
        self.pixmap = QPixmap(img_path)

        #background Qlabel
        self.background_label = QLabel(self)
        self.background_label.setScaledContents(True) #automaically scale to fit
        self.background_label.setMouseTracking(True)
        self.background_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.update_background()

      
        label = QLabel(" ", self)
        label.setAlignment(Qt.AlignCenter)

        #layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.setContentsMargins(0, 0, 0, 0)

        #settings for dragging
        self.mouse_is_dragging = False
        self.mouse_drag_position = QPoint()
        self.setMouseTracking(True)

        #reply area
        self.reply_area = QPlainTextEdit(self)
        self.reply_area.setPlainText("")
        self.reply_area.setReadOnly(True)
        self.reply_area.setFixedSize(540,250)
        self.reply_area.setStyleSheet("""
            background-color: white;
            border: none;
            font-family: '微軟正黑體 Light';
            font-size:16px;
            color: rgba(0,0,0,150);
            line-height: 150%;
        """)
        self.reply_area.setGeometry(26,78,550,73)

        #input box
        self.input_box = QTextEdit(self)
        self.input_box.setPlaceholderText("")
        self.input_box.setFixedSize(550,73)
        self.input_box.setStyleSheet("""
            QTextEdit{
                background-color: white;
                border: none;
                font-family: 'Comic Sans MS';
                font-size: 15px;
            }
        """)
        self.input_box.setGeometry(23,353,550,73)

        #send button
        self.send_button = QPushButton("Send", self)
        self.send_button.setFixedSize(60,30)
        '''
        self.send_button.setStyleSheet("""
            border-radius: 5px;
            border-color:1px solid purple;
            color: purple;
            background-color: rgba(190, 160, 206, 206);
            font-family: 'Comic Sans MS';
            font-weight: bold;
        """)
        '''
        self.send_button.move(510,390)
        self.send_button.clicked.connect(self.handle_send)

        #thread
        self.current_thread_id = "thread_gWYQtMUDzCaOVevawWBHTjwe"

        #Combobox for threads
        self.thread_selector = QComboBox(self)
        self.thread_selector.addItem("Chat 1", "thread_viYMHiRdWbF1uKul2pimdq2T")
        self.thread_selector.addItem("Daily Planning", "thread_ZeDc9lBLx03HWPSP2tnsQxZH")
        self.thread_selector.addItem("heart 2 heart", "thread_W0wQgMj82xp7btUWMg8Zuy5f")
        self.thread_selector.addItem("Test and Debug", "thread_gWYQtMUDzCaOVevawWBHTjwe")
        self.thread_selector.setGeometry(20,20,200,30)
        self.thread_selector.currentIndexChanged.connect(self.on_thread_selected)

    def update_background(self):
        if not self.pixmap.isNull():
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.resize(self.size())
            self.background_label.lower()

    def mousePressEvent(self,e):
        if e.button() == Qt.LeftButton:
            self.mouse_is_dragging = True
            self.mouse_drag_position = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()
    
    def mouseMoveEvent(self ,e):
        if  self.mouse_is_dragging and (e.buttons() & Qt.LeftButton):
            self.move(e.globalPos() - self.mouse_drag_position)
            e.accept()

    def mouseReleaseEvent(self, e):
        self.mouse_is_dragging = False

    #show commend response on gui
    def show_info(self, message:str):
        self.reply_area.appendHtml(f"""
            <div style='color: black; font-style:italic; font-size:30px; margin:20px 0;'>{message}</div>
        """)

    @staticmethod
    def get_thread_id_by_name(name: str):
        return THREAD_NAME_ID_MAP.get(name)

    @staticmethod
    def get_thread_name_by_id(thread_id: str):
        for k, v in THREAD_NAME_ID_MAP.items():
            if v == thread_id:
                return k

    def on_thread_selected(self,index):
        thread_id = self.thread_selector.itemData(index)
        self.switch_thread(thread_id)

    def switch_thread(self, thread_id):
        self.current_thread_id = thread_id
        thread_name = get_thread_title_by_id(thread_id)
        self.show_info("[Switched to: {thread_name} 🌼 :))]")

    def switch_thread_prompt(self):
        read_thread = input("Switch to Thread:\n1: Chat1\n2: daily_planning\n3: life_talk\n4: TestChatTheme1\n\nExecute: ").strip()
        if read_thread == "1":
            self.switch_thread("thread_viYMHiRdWbF1uKul2pimdq2T")
        elif read_thread == "2":
            self.switch_thread("thread_ZeDc9lBLx03HWPSP2tnsQxZH")
        elif read_thread == "3":
            self.switch_thread("thread_W0wQgMj82xp7btUWMg8Zuy5f")
        elif read_thread == "4":
            self.switch_thread("thread_gWYQtMUDzCaOVevawWBHTjwe")
        else:
            self.show_info("[Invalid option 🌼 :))]")

    def show_thread_history(self):
        try: 
            messages = read_thread_messages(self.current_thread_id)
            self.show_info("--------------History--------------")
            for msg in messages:
                if msg['role']== "user":
                    self.reply_area.appendPlainText(f"我: {msg['content']}")
                elif msg['role'] == "assistant":
                    self.reply_area.appendPlainText(f"精靈: {msg['content']}")

        except Exception as e:
            logging.error(f"[Error reading thread historty] {e}")

    def read_thread_prompt(self):
        num_choice = input("Read Thread:\n1: Chat1\n2: daily_planning\n3: life_talk\n4: TestChatTheme1\n\nExecute: ").strip()
        read_thread_id = THREAD_NUM_ID_MAP.get(num_choice)
        if not read_thread_id:
            self.show_info("[Invalid thread number!]")

        self.show_info("\n")
        self.show_info(f"[🍓🍒❣️ Conversation logs from <b>{get_thread_title_by_id(read_thread_id)}]")

        read_thread_messages(read_thread_id)

    def create_thread_prompt(self):
        try:
            #input new title
            self.show_info("Input new thread title:")         
            title = self.input_box.toPlainText().strip()

            #choose category
            self.show_info("Choose its category: \n1: Chat1 2: daily_planning 3: life_talk\n")  
            
            num_choice = self.input_box.toPlanText().stip()
            if num_choice =="1":
                category = "Chat"
            if num_choice =="2":
                category = "daily_planning"
            if num_choice =="3":
                category = "life_talk"
            else:
                self.show_info("[Unsupported Input! 😧]")
                return

            thread_id = create_thread(title=title, category=category)
            self.show_info(f"[Created Successfully ✅\nTitle: {title}\nThread ID: {thread_id}]")        

        except Exception as e:
            logging.error(f"[Error] failed to create thread {e}")
            self.show_info("[Failed to create thread\n]")

    def handle_user_commend(self, user_input: str):
        cmd = user_input.strip().lower()

        #list thread commend
        if cmd == "\\list":
            try:
                threads = list_threads()
                if not threads:
                    self.show_info("[Thread List 是空的或讀取失敗 🫠]")
                    return True

                self.show_info("[Thread List 📜]")
                for idx, row in enumerate(threads, start=1):
                    thread_title = row[1] or "(Untitled)"
                    thread_category = row[2] or "(Uncategorized)"
                    token_usage = row[3]
                    thread_id = row[0]
                    self.show_info(f"{idx}. {thread_title}｜分類: {thread_category}｜Tokens: {token_usage}｜ID: {thread_id}")
            except Exception as e:
                logging.error(f"[Error in \\list] {e}")
                self.show_info("[⚠️ 發生錯誤，無法列出 threads]")
            return True


        #switch thread commend
        elif cmd.startswith("\\switch"):
            parts = cmd.split()
            if len(parts) < 2:
                self.show_info("[請輸入 thread 編號，如：\\switch 2]")
                self.show_info("(目前可用編號如下：)")
                for idx, (title, tid) in enumerate(THREAD_NAME_ID_MAP.items(), start=1):
                    self.show_info(f"{idx}. {title}  ➤  {tid}")
                return True

            thread_index = parts[1]
            thread_id = THREAD_NUM_ID_MAP.get(thread_index)
            if thread_id:
                self.switch_thread(thread_id)
            else:
                self.show_info("[Invalid thread number! ❌]")
            return True

        #read thread commend
        elif cmd.startswith("\\read"):
            parts = cmd.split()
            if len(parts) < 2:
                self.show_info("[請輸入 thread 編號，如：\\read 3]")
                self.show_info("(目前可用編號如下：)")
                for idx, (title, tid) in enumerate(THREAD_NAME_ID_MAP.items(), start=1):
                    self.show_info(f"{idx}. {title}  ➤  {tid}")
                return True

            thread_index = parts[1]
            thread_id = THREAD_NUM_ID_MAP.get(thread_index)
            if not thread_id:
                self.show_info("[Invalid thread number! ❌]")
                return True

            try:
                self.show_info(f"📖 [Reading from {get_thread_title_by_id(thread_id)}]")
                messages = read_thread_messages(thread_id)
                for msg in messages:
                    if msg["role"] == "user":
                        self.reply_area.appendPlainText(f"我: {msg['content']}")
                    elif msg["role"] == "assistant":
                        self.reply_area.appendPlainText(f"精靈: {msg['content']}")
            except Exception as e:
                logging.error(f"[Error reading thread :((] {e}")
                self.show_info("[讀取失敗]")
            return True

        #create thread command
        elif cmd.startswith("\\create"):
            parts = cmd.split(maxsplit=2)
            if len(parts) < 3:
                self.show_info("[請輸入格式：\\create 標題 分類]\nEx: \\create 測試 daily_planning")
                return True

            title = parts[1]
            category = parts[2]

            try:
                thread_id = create_thread(title=title, category=category)
                self.show_info(f"[Created ✅ Title: {title} | ID: {thread_id}]")
            except Exception as e:
                logging.error(f"[Create Error] {e}")
                self.show_info("[Failed to create :(((]")
            return True

        return False

            
    
    def handle_send(self):
        user_input = self.input_box.toPlainText().strip()
        print(f"[DEBUG] 使用者輸入: {user_input}")
        if self.handle_user_commend(user_input):
            return

        # append user text to reply area
        user_html = f"""
            <div style = "margin-bottom:10px; font-family:'微軟正黑體 Light', 'Comic Sans MS'; font-size:15px; line-height: 1.3;">
                <b>芍芍:</b> <span>{user_input}</span>
            </div>
        """
        self.reply_area.appendHtml(user_html)

        # send from chat client
        try:
            response = send(self.current_thread_id, user_input)
            elfie_html = f"""
                <div style= "margin-bottom: 15px; font-family:'微軟正黑體 Light', 'Comic Sans MS'; font-size:15px; line-height: 1.3;">
                    <b>精靈:</b> <span>{response}</span>
                </div>
            """
            self.reply_area.appendHtml(elfie_html)
        except Exception as e:
            logging.error(f"[Error: Failed to handle send! ] {e}")

        self.input_box.clear()


if  __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = TypeWindow()
    window.show()
    sys.exit(app.exec_())
