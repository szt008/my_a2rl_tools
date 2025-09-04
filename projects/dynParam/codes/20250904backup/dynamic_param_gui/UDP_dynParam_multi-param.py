import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QDialog
from PyQt5.QtCore import Qt
import socket
import json
import threading
from lib.dynamic_param_widget import DynParamWidget
from lib.config_widget import ConfigWidget
import signal
import yaml

class UdpParamWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UDP Param Sender')
        self.setGeometry(100, 100, 600, 100)

        # show window in the center of the screen
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        layout = QGridLayout(self)

        # Add config file input and load button at the top (left)
        self.load_config_widget = ConfigWidget("Load", self.load_config)
        layout.addWidget(self.load_config_widget, 0, 0, 1, 1)

        # Add save config input and save button at the top (right)
        self.save_config_widget = ConfigWidget("Save", self.save_config)
        layout.addWidget(self.save_config_widget, 0, 2, 1, 1)

        layout.setHorizontalSpacing(30)  # Increase horizontal spacing between columns

        current_start_row = 1

        self.param_widgets = []
        item_num = 12
        for i in range(item_num):
            widget = DynParamWidget(self)
            row = i // 2 + current_start_row
            col = i % 2
            layout.addWidget(widget, row, col*2)
            self.param_widgets.append(widget)

        current_start_row += item_num // 2

        self.send_btn = QPushButton('Send UDP', self)
        self.send_btn.clicked.connect(self.send_udp)
        layout.addWidget(self.send_btn, current_start_row, 0, 1, 3)  # Shift down by 1 row
        current_start_row += 1

        # 启动监听线程
        threading.Thread(target=self.listen_feedback, daemon=True).start()

    def load_config(self, path):

        def guess_type(val):
            s = str(val).strip().lower()
            if s in ['True', 'False', 'true', 'false', 'yes', 'no', 'on', 'off']:
                return 'bool'
            try:
                int_val = int(s)
                if '.' not in s:
                    return 'int'
            except ValueError:
                pass
            try:
                float(s)
                return 'float'
            except ValueError:
                pass
            return 'str'

        try:
            with open(path, 'r') as f:
                param_dict = yaml.safe_load(f)
                item_count = 0
                for node, ros_params in param_dict.items():
                    params = ros_params['ros__parameters']
                    for param, info in params.items():
                        if item_count > len(self.param_widgets):
                            print("Warning: More parameters in config than available widgets.")
                            return
                        self.param_widgets[item_count].node_input.setText(node)
                        self.param_widgets[item_count].param_input.setText(param)
                        self.param_widgets[item_count].type_combo.setCurrentText(guess_type(info))
                        self.param_widgets[item_count].value_input.setText(str(info))
                        
                        item_count += 1
            print(f"Loaded param_dict from {path}")
        except Exception as e:
            print(f"Failed to load config: {e}")

    def save_config(self, path):
        param_dict = {}
        for widget in self.param_widgets:
            node = widget.node_input.text()
            param = widget.param_input.text()
            value = widget.value_input.text()
            param_type = widget.type_combo.currentText()
            if not param:
                continue
            if param_type == 'float':
                try:
                    fval = float(value)
                    if fval == int(fval):
                        value = float('{:.1f}'.format(fval))
                    else:
                        value = fval
                except Exception:
                    pass
            elif param_type == 'int':
                try:
                    value = int(value)
                except Exception:
                    pass
            elif param_type == 'bool':
                value = str(value).strip().lower() in ['true', '1', 'yes', 'on']
            else:
                value = str(value)
            if node not in param_dict:
                param_dict[node] = {'ros__parameters': {}}
            param_dict[node]['ros__parameters'][param] = value
        with open(path, 'w') as f:
            yaml.dump(param_dict, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        print(f"Save config to: {path}")

    def send_udp(self):
        data_list = []
        for widget in self.param_widgets:
            node = widget.node_input.text()
            param = widget.param_input.text()
            value = widget.value_input.text()
            param_type = widget.type_combo.currentText()
            if not param or not widget.get_lamp_color() == 'blue':
                continue
            param_item = {
                'node': node,
                'param': param,
                'value': value,
                'type': param_type
            }
            data_list.append(param_item)
            widget.set_lamp_color('red')
            
        if not data_list:
            return
        msg = json.dumps(data_list).encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, ('127.0.0.1', 9999))
        sock.close()

    def listen_feedback(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', 10000))
        while True:
            data, addr = sock.recvfrom(1024)
            data_dict = json.loads(data)
            node_name = data_dict['node']
            param_name = data_dict['param']
            param_set_success = data_dict['Success']
            # 匹配所有widget内容
            for widget in self.param_widgets:
                if (param_set_success and
                    node_name == widget.node_input.text() and
                    param_name == widget.param_input.text()):
                    widget.set_lamp_color('green')
    

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # 允许Ctrl+C关闭PyQt窗口
    app = QApplication(sys.argv)
    win = UdpParamWindow()
    win.show()
    sys.exit(app.exec_())