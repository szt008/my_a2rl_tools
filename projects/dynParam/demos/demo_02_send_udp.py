import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
import socket

class UdpSender(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UDP Sender')
        self.setGeometry(100, 100, 200, 100)
        btn = QPushButton('Send UDP', self)
        btn.clicked.connect(self.send_udp)
        btn.resize(180, 40)
        btn.move(10, 30)

    def send_udp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = b'hello from pyqt'
        sock.sendto(msg, ('127.0.0.1', 9999))
        sock.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sender = UdpSender()
    sender.show()
    sys.exit(app.exec_())