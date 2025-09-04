from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox

class DynParamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        # Node input
        self.node_input = QLineEdit(self)
        self.node_input.setMinimumWidth(200)
        layout.addWidget(QLabel('Node:'))
        layout.addWidget(self.node_input)

        # Parameter name input
        self.param_input = QLineEdit(self)
        self.param_input.setMinimumWidth(150)
        layout.addWidget(QLabel('Parameter:'))
        layout.addWidget(self.param_input)

        # Type selection
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(['float', 'int', 'string', 'bool', 'list_float'])
        layout.addWidget(QLabel('Type:'))
        layout.addWidget(self.type_combo)

        # Value input
        self.value_input = QLineEdit(self)
        layout.addWidget(QLabel('Value:'))
        layout.addWidget(self.value_input)

        # Status lamp
        self.lamp = QLabel()
        self.lamp.setFixedSize(16, 16)
        self.set_lamp_color('green')
        layout.addWidget(self.lamp)

        # Change lamp to blue on any content change
        self.value_input.textChanged.connect(lambda: self.set_lamp_color('blue'))

    def set_lamp_color(self, color):
        self.lamp_color = color
        self.lamp.setStyleSheet(f'background-color: {color}; border-radius: 8px; border: 1px solid #333;')

    def get_lamp_color(self):
        return self.lamp_color