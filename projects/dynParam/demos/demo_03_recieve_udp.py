import rclpy
from rclpy.node import Node
import socket
import threading

class UdpReceiverNode(Node):
    def __init__(self):
        super().__init__('udp_receiver')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 9999))
        thread = threading.Thread(target=self.listen_udp, daemon=True)
        thread.start()

    def listen_udp(self):
        while rclpy.ok():
            data, addr = self.sock.recvfrom(1024)
            print(f"Received from {addr}: {data.decode()}")

def main(args=None):
    rclpy.init(args=args)
    node = UdpReceiverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()