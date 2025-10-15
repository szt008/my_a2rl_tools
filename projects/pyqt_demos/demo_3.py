# 示例 3：QDial + QLineEdit 旋钮控制，可旋转或输入数值
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDial, QLineEdit, QLabel

class DialDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDial 示例")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.label = QLabel("当前值：0")
        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.setValue(0)
        self.dial.setNotchesVisible(True)   # 显示刻度
        self.line_edit = QLineEdit("0")

        layout.addWidget(self.dial)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 联动
        self.dial.valueChanged.connect(self.update_from_dial)
        self.line_edit.textChanged.connect(self.update_from_text)

    def update_from_dial(self, value):
        self.line_edit.setText(str(value))
        self.label.setText(f"当前值：{value}")

    def update_from_text(self, text):
        if text.isdigit():
            value = int(text)
            value = max(0, min(value, 100))
            self.dial.setValue(value)
            self.label.setText(f"当前值：{value}")

if __name__ == "__main__":
    app = QApplication([])
    w = DialDemo()
    w.show()
    app.exec_()
