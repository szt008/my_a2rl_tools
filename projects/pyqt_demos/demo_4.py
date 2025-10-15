# 运行方式：python this_file.py
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt

class NumberControl(QWidget):
    """
    一个把 QSlider 和 Q(Double)SpinBox 结合起来的通用数值控件。
    - 支持整数/小数：通过 decimals=0 使用 QSpinBox，否则 QDoubleSpinBox
    - 通过 step 控制步长，滑块以“步”为单位离散化
    """
    def __init__(self, title="参数", minimum=0.0, maximum=1.0, value=0.0, step=0.01, decimals=2, parent=None):
        super().__init__(parent)
        assert maximum > minimum, "maximum 必须大于 minimum"
        assert step > 0, "step 必须为正数"
        self.minimum = float(minimum)
        self.maximum = float(maximum)
        self.step = float(step)
        self.decimals = int(decimals)

        # 计算滑块离散步数（以 step 为单位）
        self.steps_count = int(round((self.maximum - self.minimum) / self.step))
        if self.steps_count <= 0:
            self.steps_count = 1

        # UI
        layout = QVBoxLayout(self)
        row = QHBoxLayout()
        self.label = QLabel(f"{title}")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, self.steps_count)

        # 根据 decimals 选择 SpinBox 类型
        if self.decimals == 0:
            self.spin = QSpinBox()
            self.spin.setRange(int(round(self.minimum)), int(round(self.maximum)))
            self.spin.setSingleStep(int(round(self.step)))
        else:
            self.spin = QDoubleSpinBox()
            self.spin.setDecimals(self.decimals)
            self.spin.setRange(self.minimum, self.maximum)
            self.spin.setSingleStep(self.step)

        # 排版
        row.addWidget(self.label)
        row.addWidget(self.slider, stretch=1)
        row.addWidget(self.spin, stretch=0)
        layout.addLayout(row)

        # 初始值
        self.setValue(value)

        # 信号联动（避免循环触发，使用 blockSignals）
        self.slider.valueChanged.connect(self._on_slider_changed)
        self.spin.valueChanged.connect(self._on_spin_changed)

    def _value_from_slider(self, slider_pos: int) -> float:
        # slider_pos ∈ [0, steps_count] -> 值域
        val = self.minimum + slider_pos * self.step
        if self.decimals > 0:
            # 对齐小数位
            factor = 10 ** self.decimals
            val = round(val * factor) / factor
        else:
            val = round(val)
        return min(max(val, self.minimum), self.maximum)

    def _slider_from_value(self, val: float) -> int:
        # 反向映射：值 -> slider pos
        pos = int(round((val - self.minimum) / self.step))
        return max(0, min(self.steps_count, pos))

    def _on_slider_changed(self, pos: int):
        val = self._value_from_slider(pos)
        try:
            self.spin.blockSignals(True)
            if self.decimals == 0:
                self.spin.setValue(int(round(val)))
            else:
                self.spin.setValue(val)
        finally:
            self.spin.blockSignals(False)

    def _on_spin_changed(self, val):
        # Q(Double)SpinBox 的 valueChanged 可能是 float 或 int
        val = float(val)
        pos = self._slider_from_value(val)
        try:
            self.slider.blockSignals(True)
            self.slider.setValue(pos)
        finally:
            self.slider.blockSignals(False)

    def value(self) -> float:
        return float(self.spin.value())

    def setValue(self, val: float):
        # 统一入口设置数值（会同步滑块与 spinbox）
        val = min(max(float(val), self.minimum), self.maximum)
        try:
            self.spin.blockSignals(True)
            if self.decimals == 0:
                self.spin.setValue(int(round(val)))
            else:
                self.spin.setValue(val)
        finally:
            self.spin.blockSignals(False)
        pos = self._slider_from_value(val)
        try:
            self.slider.blockSignals(True)
            self.slider.setValue(pos)
        finally:
            self.slider.blockSignals(False)


# ==== 演示窗口：一个小数控件 + 一个整数控件 ====
class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QSlider + Q(Double)SpinBox 结合示例")
        self.resize(520, 160)
        layout = QVBoxLayout(self)

        # 小数：-10.00 ~ 10.00，步长 0.10，保留 2 位小数
        self.ctrl_double = NumberControl(
            title="增益(浮点)：",
            minimum=-10.0, maximum=10.0, value=1.2,
            step=0.10, decimals=2
        )
        # 整数：0 ~ 100，步长 5
        self.ctrl_int = NumberControl(
            title="阈值(整数)：",
            minimum=0, maximum=100, value=35,
            step=5, decimals=0
        )
        layout.addWidget(self.ctrl_double)
        layout.addWidget(self.ctrl_int)

        # 也可以这样读取当前值：
        # print(self.ctrl_double.value(), self.ctrl_int.value())

if __name__ == "__main__":
    app = QApplication([])
    w = Demo()
    w.show()
    app.exec_()
