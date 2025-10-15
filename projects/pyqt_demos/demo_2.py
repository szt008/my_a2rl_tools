# 示例 2：QSlider + QLineEdit 联动，可拖动或输入数值
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLineEdit, QLabel
from PyQt5.QtCore import Qt

class SliderEditDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSlider + QLineEdit 示例")
        self.resize(300, 150)

        layout = QVBoxLayout()

        self.label = QLabel("当前值：0")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(0)
        self.line_edit = QLineEdit("0")

        layout.addWidget(self.slider)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # 信号连接
        self.slider.valueChanged.connect(self.update_from_slider)
        self.line_edit.textChanged.connect(self.update_from_text)

    def update_from_slider(self, value):
        self.line_edit.setText(str(value))
        self.label.setText(f"当前值：{value}")

    def update_from_text(self, text):
        if text.isdigit():
            value = int(text)
            value = max(0, min(value, 100))  # 限制范围
            self.slider.setValue(value)
            self.label.setText(f"当前值：{value}")

if __name__ == "__main__":
    app = QApplication([])
    w = SliderEditDemo()
    w.show()
    app.exec_()
