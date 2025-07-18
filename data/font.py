from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont
import sys

font_list = [
    "微軟正黑體",
    "微軟正黑體 Light",
    "新細明體",
    "新細明體-ExtB",
    "標楷體",
    "細明體",
    "細明體-ExtB",
    "細明體_HKSCS",
    "細明體_HKSCS-ExtB",
    "細明體_MSCS"
]

sample_text = "精靈說：今天是個適合練習字型的好日子。"

class FontCompareWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("中文字體比較")
        self.setMinimumSize(600, 600)

        layout = QVBoxLayout()

        for font_name in font_list:
            label = QLabel(f"{font_name}:")
            label.setStyleSheet("font-weight: bold; margin-top: 10px;")
            layout.addWidget(label)

            text = QTextEdit()
            text.setReadOnly(True)
            text.setText(sample_text)
            text.setFont(QFont(font_name, 14))
            text.setFixedHeight(50)
            layout.addWidget(text)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FontCompareWindow()
    window.show()
    sys.exit(app.exec_())
