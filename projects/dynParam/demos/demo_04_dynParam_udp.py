import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox
from PyQt5.QtCore import Qt
import socket
import json
import threading

class UdpParamSender(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UDP Param Sender')
        self.setGeometry(100, 100, 400, 250)
        layout = QVBoxLayout(self)

        self.node_input = QLineEdit(self)
        self.node_input.setText('/eav24/lqr_control_node')
        layout.addWidget(QLabel('Node Name:'))
        layout.addWidget(self.node_input)

        self.param_input = QLineEdit(self)
        self.param_input.setText('control_Cd0')
        layout.addWidget(QLabel('Param Name:'))
        layout.addWidget(self.param_input)

        self.type_label = QLabel('Param Type:')
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(['float', 'int', 'string'])
        self.type_combo.setCurrentText('float')
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        self.value_input = QLineEdit(self)
        self.value_input.setText('1.0')
        self.value_input.setPlaceholderText('Value')
        layout.addWidget(QLabel('Value:'))
        layout.addWidget(self.value_input)


        btn = QPushButton('Send UDP', self)
        btn.clicked.connect(self.send_udp)
        layout.addWidget(btn)

        # 绑定内容变动信号
        self.node_input.textChanged.connect(lambda: self.set_lamp_color('blue'))
        self.param_input.textChanged.connect(lambda: self.set_lamp_color('blue'))
        self.value_input.textChanged.connect(lambda: self.set_lamp_color('blue'))
        self.type_combo.currentIndexChanged.connect(lambda: self.set_lamp_color('blue'))

        self.lamp = QLabel()
        self.lamp.setFixedSize(16, 16)
        self.set_lamp_color('green')
        layout.addWidget(self.lamp, alignment=Qt.AlignCenter)

        # 启动监听线程，监听本地 10000 端口的 param set 回传
        threading.Thread(target=self.listen_feedback, daemon=True).start()

    def set_lamp_color(self, color):
        self.lamp.setStyleSheet(f'background-color: {color}; border-radius: 8px; border: 1px solid #333;')

    def send_udp(self):
        value = self.value_input.text()
        param_type = self.type_combo.currentText()
        # 检查类型和值是否匹配
        type_ok = True
        if param_type == 'float':
            try:
                float(value)
            except ValueError:
                type_ok = False
        elif param_type == 'int':
            try:
                int(value)
            except ValueError:
                type_ok = False
        # string类型无需检查
        if not type_ok:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Type Error', f'Value does not match type {param_type}!')
            return
        param_item = {
            'node': self.node_input.text(),
            'param': self.param_input.text(),
            'value': value,
            'type': param_type
        }
        data_list = [param_item]
        msg = json.dumps(data_list).encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, ('127.0.0.1', 9999))
        sock.close()
        self.set_lamp_color('red')

    def listen_feedback(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 10000))  # 假设param set回传UDP到10000端口
        while True:
            data, addr = sock.recvfrom(1024)
            # 你可以根据内容判断是否为param set反馈
            data_dict = json.loads(data)
            print("UDP received: " + str(data_dict))

            node_name = data_dict['node']
            param_name = data_dict['param']
            param_set_success = data_dict['Success']

            if param_set_success and node_name == self.node_input.text() and param_name == self.param_input.text():
                self.set_lamp_color('green')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sender = UdpParamSender()
    sender.show()
    sys.exit(app.exec_())