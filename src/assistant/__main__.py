# assistant/__main__.py
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from db import init_db
import sys

import logging
 
 
logging.basicConfig(
    level=logging.ERROR,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)


def main():
    logging.info("Start Application")
    app = QApplication(sys.argv)
    window = MainWindow(show_type_window = True)
    window.show()
    init_db()
    sys.exit(app.exec_())

if __name__ =="__main__":
    main()