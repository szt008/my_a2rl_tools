# 示例 1：QDoubleSpinBox 可直接输入或滚动调整
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDoubleSpinBox, QLabel

class SpinBoxDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDoubleSpinBox 示例")
        self.resize(300, 100)

        layout = QVBoxLayout()

        self.label = QLabel("当前值：0.00")
        self.spin = QDoubleSpinBox()
        self.spin.setRange(-10.0, 10.0)
        self.spin.setSingleStep(0.1)     # 步长
        self.spin.setDecimals(2)         # 保留两位小数
        self.spin.setValue(0.0)

        layout.addWidget(self.spin)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.spin.valueChanged.connect(self.update_label)

    def update_label(self, value):
        self.label.setText(f"当前值：{value:.2f}")

if __name__ == "__main__":
    app = QApplication([])
    w = SpinBoxDemo()
    w.show()
    app.exec_()
