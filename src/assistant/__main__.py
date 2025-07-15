# assistant/__main__.py
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys
import logging

logging.basicConfig(
    level = logging.INFO,
    format = '[%(astime)s [%(levelname)s] %(message)s',
    handler = [logging.StreamHandler()]
)

def main():
    logging.info("Start Application")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ =="__main__":
    main()

