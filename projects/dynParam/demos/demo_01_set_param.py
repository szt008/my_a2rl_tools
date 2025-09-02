import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import SetParameters
from rclpy.parameter import Parameter

def main():
    rclpy.init()
    node = Node('param_setter')
    client = node.create_client(SetParameters, '/eav24/lqr_control_node/set_parameters')
    while not client.wait_for_service(timeout_sec=1.0):
        print('Waiting for parameter service...')
    req = SetParameters.Request()
    param = Parameter('control_Cd0', Parameter.Type.DOUBLE, 1.0)
    req.parameters = [param.to_parameter_msg()]
    future = client.call_async(req)
    rclpy.spin_until_future_complete(node, future)
    if future.result() is not None:
        print('Parameter set result:', future.result().results[0].successful)
    else:
        print('Failed to set parameter')
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# 注意如果conda中没有安装ros2，该demo需要使用系统默认python环境运行