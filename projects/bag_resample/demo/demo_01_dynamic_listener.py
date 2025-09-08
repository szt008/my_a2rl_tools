import rclpy
from rclpy.node import Node
import yaml
import importlib

class YamlListener(Node):
    def __init__(self, yaml_path):
        super().__init__('yaml_listener')
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        self.vars = {}
        for var, info in config.items():
            topic = info['topic']
            field = info['field']
            # 获取topic类型
            topic_type = self.get_topic_type(topic)
            if topic_type is None:
                self.get_logger().warning(f"Cannot get type for {topic}")
                continue
            msg_module_name, msg_class_name = topic_type.rsplit('/', 1)
            msg_module = importlib.import_module(msg_module_name.replace('/', '.'))
            msg_class = getattr(msg_module, msg_class_name)
            self.create_subscription(
                msg_class,
                topic,
                self.make_callback(var, field),
                10
            )
            self.get_logger().info(f"Listening {var} from {topic}.{field}")

    def get_topic_type(self, topic):
        # 通过ros2 topic info命令获取类型
        import subprocess
        try:
            out = subprocess.check_output(['ros2', 'topic', 'info', topic], encoding='utf-8')
            for line in out.splitlines():
                if line.startswith('Type:'):
                    return line.split('Type:')[1].strip()
        except Exception as e:
            self.get_logger().error(str(e))
        return None

    def make_callback(self, var, field):
        def callback(msg):
            value = getattr(msg, field, None)
            self.vars[var] = value
            self.get_logger().info(f"{var} = {value}")
        return callback

def main():
    import sys
    rclpy.init()
    node = YamlListener(sys.argv[1] if len(sys.argv) > 1 else 'config.yaml')
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()