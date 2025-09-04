from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtWidgets import QFrame, QLineEdit, QHBoxLayout

class ConfigWidget(QWidget):
    def __init__(self, button_str, config_function, parent=None, ):
        super().__init__(parent)
        layout = QHBoxLayout(self)

        self.config_lineedit = QLineEdit(self)
        self.config_lineedit.setText('./src/car_gui/dynamic_param_gui/param/default.yaml')
        self.config_lineedit.setFixedWidth(500)
        layout.addWidget(self.config_lineedit)
        self.load_btn = QPushButton(button_str, self)
        layout.addWidget(self.load_btn)
        self.load_btn.clicked.connect(lambda: config_function(self.config_lineedit.text()))