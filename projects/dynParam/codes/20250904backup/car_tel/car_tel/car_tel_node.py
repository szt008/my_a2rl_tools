import rclpy
from rclpy.node import Node
from rclpy.serialization import serialize_message
from rcl_interfaces.srv import SetParameters
from rclpy.parameter import Parameter
from sd_msgs.msg import CarTel, RaceControlReport, StateEstimation, VehicleInputs
from can_bus_handler.msg import RcStatus01, WheelsSpeed01, Badenia560BrakeDiskTemp, BSUStatus01, ICEStatus02, Badenia560TpmsFront, Badenia560TpmsRear, KistlerVelAngle
from vectornav_msgs.msg import GpsGroup, CommonGroup
from autonoma_msgs.msg import GroundTruth, GroundTruthArray
from geometry_msgs.msg import PoseWithCovariance, Pose2D
from sensor_msgs.msg import PointCloud2
import threading
import time
import pymap3d
import numpy as np
from tf_transformations import euler_from_quaternion
import socket
import json

class CarTelNode(Node):
    def __init__(self):
        super().__init__('car_tel_node')
        self.lock = threading.Lock()  # Protect shared_message

        # UDP sender configuration
        self.declare_parameter('mode', 'remote')  # 'local'(publishing ros2 topic) or 'remote' (sending UDP packets to a remote client (with receiver))
        self.declare_parameter('udp_host', '127.0.0.1')
        self.declare_parameter('udp_port', 6672)
        self.declare_parameter('data_format', 'pickle')  # 'pickle' or 'json'
        self.mode = self.get_parameter('mode').get_parameter_value().string_value
        self.udp_host = self.get_parameter('udp_host').get_parameter_value().string_value
        self.udp_port = self.get_parameter('udp_port').get_parameter_value().integer_value
        self.data_format = self.get_parameter('data_format').get_parameter_value().string_value

        # UDP socket setup for remote mode
        self.udp_socket = None
        if self.mode == 'remote':
            self.setup_udp_socket()
                                    
        # Misc
        self.wheel_radius = 0.307
        self.lat0 = 34.84430072
        self.lon0 = 136.53385609
        self.x_offset = 0.0
        self.y_offset = 0.0
        

        # self.vehicle_flags = ["safe_stop","orange","purple","pit_in","blue","idle","unknown","null","black/white"]
        self.vehicle_flags = {
            18: "black/white",
            0: "green",
            31: "long_lap",
            40: "pit_in",
            3: "blue"
        }

        # self.track_flags = ["red","yellow_full_course","green","checkered","code60","warmup","identification"]
        self.track_flags = {
            11: "yellow_full_course",
            0: "green",
            5: "red",
            13: "code60",
        }
        
        self.sector_flags = {
            1: "local_yellow",
            4: "green",
            0: "clear"
        }
        
        self.session_types = {
            0: "clear",
            16: "chequered",
            64: "pratice",
            128: "qualify",
            192: "race"
        }
        
        
        # Car Telemetry Publisher
        self.car_tel_pub = self.create_publisher(CarTel, 'car_tel', 10)
        self.timer = self.create_timer(0.01, self.publish_car_tel)
        self.topic_hz_timer = self.create_timer(1.0, self.clear_topic_hz)
        self.shared_message = CarTel()

        # UDP Listener
        if self.mode == 'remote':
            self.udp_socket.bind(('0.0.0.0', 9999)) # necessary for receiving UDP packets
            self.udp_listener_thread = threading.Thread(target=self.listen_udp_data, daemon=True)
            self.udp_listener_thread.start()

        # Clients for Dynamic Parameters (Support multiple nodes by using a dict: {node_name: client})
        self.dynParam_clients = {}
        self.dynParam_nodes = ['/eav24/lqr_control_node', 
                               '/eav24/trajserver_node', 
                               '/eav24/state_estimation_node']  # Add more node names as needed
        for node_name in self.dynParam_nodes:
            self.dynParam_clients[node_name] = self.create_client(SetParameters, f'{node_name}/set_parameters')

        # Subscribers
        self.wheels_speed_sub = self.create_subscription(WheelsSpeed01, 'can/wheels_speed_01', self.wheels_speed_callback, 1)
        self.brake_disk_temp_sub = self.create_subscription(Badenia560BrakeDiskTemp, 'can/badenia_560_brake_disk_temp', self.brake_disk_temp_callback, 1)
        self.bsu_status_01_sub = self.create_subscription(BSUStatus01, 'can/bsu_status_01', self.bsu_status_01_callback, 1)
        self.ice_status_02_sub = self.create_subscription(ICEStatus02, 'can/ice_status_02', self.ice_status_02_callback, 1)
        self.tpms_front_sub = self.create_subscription(Badenia560TpmsFront, 'can/badenia_560_tpms_front', self.tpms_front_callback, 1)
        self.tpms_rear_sub = self.create_subscription(Badenia560TpmsRear, 'can/badenia_560_tpms_rear', self.tpms_rear_callback, 1)
        self.vel_angle_sub = self.create_subscription(KistlerVelAngle, 'can/kistler_vel_angle', self.vel_angle_callback, 1)
        self.gps_sub = self.create_subscription(GpsGroup, 'vectornav/raw/gps', self.gps_callback, 1)
        self.gps2_sub = self.create_subscription(GpsGroup, 'vectornav/raw/gps2', self.gps2_callback, 1)
        self.common_sub = self.create_subscription(CommonGroup, 'vectornav/raw/common', self.common_callback, 1)
        self.state_estimation_sub = self.create_subscription(StateEstimation, 'state_estimation_gt', self.state_estimation_callback, 1)
        self.race_control_report_sub = self.create_subscription(RaceControlReport, 'race_control', self.race_control_report_callback, 1)
        self.vehicle_inputs_sub = self.create_subscription(VehicleInputs, 'vehicle_inputs', self.vehicle_inputs_callback, 1)
        self.lidar_pose_sub = self.create_subscription(PoseWithCovariance, 'lidar_localization/ndt_pose_with_covariance', self.lidar_pose_callback, 1)
        self.lidar_front_sub = self.create_subscription(PointCloud2, 'sensor/lidar_front/points', self.lidar_front_callback, 1)
        self.lidar_right_sub = self.create_subscription(PointCloud2, 'sensor/lidar_right/points', self.lidar_right_callback, 1)
        self.lidar_left_sub = self.create_subscription(PointCloud2, 'sensor/lidar_left/points', self.lidar_left_callback, 1)
        self.opponent_sub = self.create_subscription(GroundTruthArray, 'v2v_ground_truth', self.opponent_callback, 10)
        self.rc_status_sub = self.create_subscription(RcStatus01, 'can/rc_status_01', self.rc_status_callback, 1)
        
        self.topic_hz = {
            'can/wheels_speed_01': 0,
            'can/badenia_560_brake_disk_temp': 0,
            'can/bsu_status_01': 0,
            'can/ice_status_02': 0,
            'can/badenia_560_tpms_front': 0,
            'can/badenia_560_tpms_rear': 0,
            'can/kistler_vel_angle': 0,
            'vectornav/raw/gps': 0,
            'vectornav/raw/gps2': 0,
            'vectornav/raw/common': 0,
            'state_estimation_gt': 0,
            'race_control': 0,
            'vehicle_inputs': 0,
            'lidar_localization/ndt_pose_with_covariance': 0,
            'sensor/lidar_front/points': 0,
            'sensor/lidar_right/points': 0,
            'sensor/lidar_left/points': 0,
            'v2v_ground_truth': 0,
            'can/rc_status_01': 0
        }
        
        self.last_kistler_recieve_time = 0
        self.last_wheel_speed_recieve_time = 0
        self.last_gps_recieve_time = 0
        self.last_gps2_recieve_time = 0
        self.last_common_recieve_time = 0
        self.last_lidar_loc_recieve_time = 0
        self.last_lidar_front_recieve_time = 0
        self.last_lidar_right_recieve_time = 0
        self.last_lidar_left_recieve_time = 0
        
        self.shared_message.localization_poses.append(Pose2D(x=0.0, y=0.0, theta=0.0))
        self.shared_message.localization_poses.append(Pose2D(x=0.0, y=0.0, theta=0.0))
        self.shared_message.localization_poses.append(Pose2D(x=0.0, y=0.0, theta=0.0))
        
        self.get_logger().info(f"CarTel initialized in {self.mode} mode")
        if self.mode == 'remote':
            self.get_logger().info(f"UDP target: {self.udp_host}:{self.udp_port}")

    def setup_udp_socket(self):
        """Setup UDP socket for remote telemetry transmission"""
        try:
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.get_logger().info("UDP socket created successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to create UDP socket: {e}")
            self.udp_socket = None

    def send_udp_data(self, msg):
        """Send ROS message via UDP using rclpy serialization"""
        if self.udp_socket is None:
            return
        
        try:
            # Serialize the ROS message directly
            serialized_data = serialize_message(msg)
            
            # Send data
            self.udp_socket.sendto(serialized_data, (self.udp_host, self.udp_port))
            
        except Exception as e:
            self.get_logger().error(f"Failed to send UDP data: {e}")

    def listen_udp_data(self):
        if self.udp_socket is None:
            self.get_logger().warn("UDP socket is not initialized, listen_udp_data will exit.")
            return
        while rclpy.ok():
            self.get_logger().info("UDP listening...")
            data, addr = self.udp_socket.recvfrom(1024)
            data_str = data.decode()
            print(f"Received from {addr}: {data_str}")
            data_dict_list = json.loads(data_str)
            for data_dict in data_dict_list:
                node_name = data_dict['node']
                param_name = data_dict['param']
                param_type_str = data_dict['type']
                value_str = data_dict['value']
                
                if param_type_str == 'float':
                    param_type = Parameter.Type.DOUBLE
                    value = float(value_str)
                elif param_type_str == 'int':
                    param_type = Parameter.Type.INTEGER
                    value = int(value_str)
                else:
                    param_type = Parameter.Type.STRING
                    value = value_str

                req = SetParameters.Request()
                req.parameters = [Parameter(param_name, param_type, value).to_parameter_msg()]
                future = self.dynParam_clients[node_name].call_async(req)
                rclpy.spin_until_future_complete(self, future)

                if future.result() is not None:
                    self.get_logger().info(f'Parameter set result: {future.result().results[0].successful}.')
                    ack_udp_msg = {
                        "node": node_name,
                        "param": param_name,
                        "Success": True
                    }
                    ack_bytes = json.dumps(ack_udp_msg).encode()
                    ack_addr = (addr[0], 10000) # Force the port number to be set to 10000.
                    self.udp_socket.sendto(ack_bytes, ack_addr)
                    self.get_logger().info(f"Sent UDP ack to {ack_addr}: {ack_udp_msg}")
                else:
                    self.get_logger().error(f'Failed to set parameter.')
                        
    def publish_car_tel(self):
        gps_status = time.time() - self.last_gps_recieve_time < 0.3
        gps2_status = time.time() - self.last_gps2_recieve_time < 0.3
        common_status = time.time() - self.last_common_recieve_time < 0.1
        lidar_loc_status = time.time() - self.last_lidar_loc_recieve_time < 0.1
        lidar_front_status = time.time() - self.last_lidar_front_recieve_time < 0.1
        lidar_right_status = time.time() - self.last_lidar_right_recieve_time < 0.1
        lidar_left_status = time.time() - self.last_lidar_left_recieve_time < 0.1
        kistler_status = time.time() - self.last_kistler_recieve_time < 0.1
        wheel_speed_status = time.time() - self.last_wheel_speed_recieve_time < 0.1
        with self.lock:
            self.shared_message.sensor_status.append(int(gps_status))
            self.shared_message.sensor_status.append(int(gps2_status))
            self.shared_message.sensor_status.append(int(kistler_status))
            self.shared_message.sensor_status.append(int(wheel_speed_status))
            self.shared_message.sensor_status.append(int(common_status))
            self.shared_message.sensor_status.append(int(common_status))
            self.shared_message.sensor_status.append(int(lidar_loc_status))
            self.shared_message.sensor_status.append(int(lidar_front_status))
            self.shared_message.sensor_status.append(int(lidar_left_status))
            self.shared_message.sensor_status.append(int(lidar_right_status))
            
            if self.shared_message.engine_rpm > 500:
                self.shared_message.engine_on = 1
            
            for i in range(len(self.shared_message.localization_poses)):
                if self.shared_message.localization_poses[i].theta == -999.99:
                    self.shared_message.localization_poses[i].theta = self.shared_message.heading
            self.shared_message.header.stamp = self.get_clock().now().to_msg()

            # Publish locally if in local mode
            if self.mode == 'local':
                self.car_tel_pub.publish(self.shared_message)
            # Send via UDP if in remote mode
            elif self.mode == 'remote':
                self.send_udp_data(self.shared_message)
            else:
                self.get_logger().error(f"Unknown mode: {self.mode}. Expected 'local' or 'remote'.")
            
            self.shared_message.sensor_status = []
            
            # self.car_tel_pub.publish(self.shared_message)
            # self.shared_message.sensor_status = []
            
    def wheels_speed_callback(self, msg: WheelsSpeed01):
        self.topic_hz['can/wheels_speed_01'] = self.topic_hz['can/wheels_speed_01'] + 1
        self.last_wheel_speed_recieve_time = time.time()
        with self.lock:
            self.shared_message.wh_speed_fl = msg.wss_speed_fl_rad_s * self.wheel_radius
            self.shared_message.wh_speed_fr = msg.wss_speed_fr_rad_s * self.wheel_radius
            self.shared_message.wh_speed_rl = msg.wss_speed_rl_rad_s * self.wheel_radius
            self.shared_message.wh_speed_rr = msg.wss_speed_rr_rad_s * self.wheel_radius
            
            # Convert to m/s for fl and fr
            self.shared_message.velocity_wheel = ((self.wheel_radius * msg.wss_speed_fl_rad_s) + (self.wheel_radius * msg.wss_speed_fr_rad_s)) / 2
            
    def brake_disk_temp_callback(self, msg: Badenia560BrakeDiskTemp):
        self.topic_hz['can/badenia_560_brake_disk_temp'] = self.topic_hz['can/badenia_560_brake_disk_temp'] + 1
        with self.lock:
            self.shared_message.brake_temp_fl = msg.brake_disk_temp_fl
            self.shared_message.brake_temp_fr = msg.brake_disk_temp_fr
            self.shared_message.brake_temp_rl = msg.brake_disk_temp_rl
            self.shared_message.brake_temp_rr = msg.brake_disk_temp_rr
            
    def bsu_status_01_callback(self, msg: BSUStatus01):
        self.topic_hz['can/bsu_status_01'] = self.topic_hz['can/bsu_status_01'] + 1
        with self.lock:
            self.shared_message.bsu_status = msg.bsu_status
            
    def ice_status_02_callback(self, msg: ICEStatus02):
        self.topic_hz['can/ice_status_02'] = self.topic_hz['can/ice_status_02'] + 1
        with self.lock:
            self.shared_message.engine_oil_temp = msg.ice_oil_temp_deg_c
            self.shared_message.engine_water_temp = msg.ice_water_temp_deg_c
            self.shared_message.engine_rpm = msg.ice_engine_speed_rpm
            
    def tpms_front_callback(self, msg: Badenia560TpmsFront):
        self.topic_hz['can/badenia_560_tpms_front'] = self.topic_hz['can/badenia_560_tpms_front'] + 1
        with self.lock:
            self.shared_message.wh_temp_fl = msg.tpr4_temp_fl
            self.shared_message.wh_temp_fr = msg.tpr4_temp_fr
            
    def tpms_rear_callback(self, msg: Badenia560TpmsRear):
        self.topic_hz['can/badenia_560_tpms_rear'] = self.topic_hz['can/badenia_560_tpms_rear'] + 1
        with self.lock:
            self.shared_message.wh_temp_rl = msg.tpr4_temp_rl
            self.shared_message.wh_temp_rr = msg.tpr4_temp_rr
            
    def vel_angle_callback(self, msg: KistlerVelAngle):
        self.topic_hz['can/kistler_vel_angle'] = self.topic_hz['can/kistler_vel_angle'] + 1
        self.last_kistler_recieve_time = time.time()
        with self.lock:
            self.shared_message.velocity_kistler = msg.vel * 0.27777777777778
            
    def gps_callback(self, msg: GpsGroup):
        self.topic_hz['vectornav/raw/gps'] = self.topic_hz['vectornav/raw/gps'] + 1
        self.last_gps_recieve_time = time.time()
        with self.lock:
            e, n, u = pymap3d.geodetic2enu(msg.poslla.x, msg.poslla.y, 0.0, self.lat0, self.lon0, 0.0)
            self.shared_message.localization_poses[0] = Pose2D(x=e, y=n, theta=-999.99)
            
    def gps2_callback(self, msg: GpsGroup):
        self.topic_hz['vectornav/raw/gps2'] = self.topic_hz['vectornav/raw/gps2'] + 1
        self.last_gps2_recieve_time = time.time()
        with self.lock:
            e, n, u = pymap3d.geodetic2enu(msg.poslla.x, msg.poslla.y, 0.0, self.lat0, self.lon0, 0.0)
            self.shared_message.localization_poses[1] = Pose2D(x=e, y=n, theta=-999.99)
            
    def common_callback(self, msg: CommonGroup):
        self.topic_hz['vectornav/raw/common'] = self.topic_hz['vectornav/raw/common'] + 1
        self.last_common_recieve_time = time.time()
                    

    def lidar_pose_callback(self, msg: PoseWithCovariance):
        self.topic_hz['lidar_localization/ndt_pose_with_covariance'] = self.topic_hz['lidar_localization/ndt_pose_with_covariance'] + 1
        self.last_lidar_loc_recieve_time = time.time()
        with self.lock:
            self.shared_message.localization_poses[2] = Pose2D(x=msg.pose.position.x, y=msg.pose.position.y, theta=euler_from_quaternion(msg.pose.orientation)[2])
            
    def state_estimation_callback(self, msg: StateEstimation):
        self.topic_hz['state_estimation_gt'] = self.topic_hz['state_estimation_gt'] + 1
        self.last_state_estimation_recieve_time = time.time()
        with self.lock:
            self.shared_message.x = msg.x_m
            self.shared_message.y = msg.y_m
            self.shared_message.heading = msg.yaw_rad
            self.shared_message.covariance = 1.5
            self.shared_message.velocity = np.linalg.norm([msg.vx_mps, msg.vy_mps])
            self.shared_message.acceleration_x = msg.ax_mps2
            self.shared_message.acceleration_y = msg.ay_mps2
            
    def race_control_report_callback(self, msg: RaceControlReport):
        self.topic_hz['race_control'] = self.topic_hz['race_control'] + 1
        self.last_race_control_recieve_time = time.time()
        with self.lock:
            # self.shared_message.vehicle_flag = self.vehicle_flags[msg.vehicle_flag]
            # self.shared_message.track_flag = self.track_flags[msg.track_flag]
            # if msg.safe_stop:
            #     self.shared_message.vehicle_flag = "safe_stop"
            # if msg.emergency_stop:
            #     self.shared_message.vehicle_flag = "emergency_stop"
            self.shared_message.velocity_max = msg.max_velocity
            
    def rc_status_callback(self, msg: RcStatus01):
        self.topic_hz['can/rc_status_01'] = self.topic_hz['can/rc_status_01'] + 1
        self.last_rc_status_recieve_time = time.time()
        with self.lock:
            vf = msg.rc_car_flag
            tf = msg.rc_track_flag
            sf = msg.rc_sector_flag
            st = msg.rc_session_type
            if vf in self.vehicle_flags:
                self.shared_message.vehicle_flag = self.vehicle_flags[vf]
            else:
                self.shared_message.vehicle_flag = ""
            if tf in self.track_flags:
                self.shared_message.track_flag = self.track_flags[tf]
            else:
                self.shared_message.track_flag = ""
            if sf in self.sector_flags:
                self.shared_message.sector_flag = self.sector_flags[sf]
            else:
                self.shared_message.sector_flag = ""
            if st in self.session_types:
                self.shared_message.session_type = self.session_types[st]
            else:
                self.shared_message.session_type = ""
            
    def vehicle_inputs_callback(self, msg: VehicleInputs):
        self.topic_hz['vehicle_inputs'] = self.topic_hz['vehicle_inputs'] + 1
        self.last_vehicle_inputs_recieve_time = time.time()
        with self.lock:
            self.shared_message.throttle = msg.throttle_cmd * 100.0
            self.shared_message.brake_fl = msg.brake_fl_cmd * 100.0
            self.shared_message.brake_fr = msg.brake_fr_cmd * 100.0
            self.shared_message.brake_rl = msg.brake_rl_cmd * 100.0
            self.shared_message.brake_rr = msg.brake_rr_cmd * 100.0
            self.shared_message.steer = msg.steering_cmd * 20.3 
            self.shared_message.gear = msg.gear_cmd
            
    def opponent_callback(self, msg: GroundTruthArray):
        self.topic_hz['v2v_ground_truth'] = self.topic_hz['v2v_ground_truth'] + 1
        self.shared_message.opponents = []
        for opp in msg.vehicles:
            x, y, _ = pymap3d.geodetic2enu(opp.lat, opp.lon, 0.0, self.lat0, self.lon0, 0.0)
            self.shared_message.opponents.append(Pose2D(x=x + self.x_offset, y=y + self.y_offset, theta=((np.pi / 2) - opp.yaw)))
            
    def lidar_front_callback(self, msg: PointCloud2):
        self.topic_hz['sensor/lidar_front/points'] = self.topic_hz['sensor/lidar_front/points'] + 1
        self.last_lidar_front_recieve_time = time.time()
        
    def lidar_right_callback(self, msg: PointCloud2):
        self.topic_hz['sensor/lidar_right/points'] = self.topic_hz['sensor/lidar_right/points'] + 1
        self.last_lidar_right_recieve_time = time.time()
        
    def lidar_left_callback(self, msg: PointCloud2):
        self.topic_hz['sensor/lidar_left/points'] = self.topic_hz['sensor/lidar_left/points'] + 1
        self.last_lidar_left_recieve_time = time.time()
        
    def clear_topic_hz(self):
        temp = []
        for topic in self.topic_hz:
            temp.append(float(self.topic_hz[topic]))
            self.topic_hz[topic] = 0
        self.shared_message.topic_hz = temp
        
    def __del__(self):
        """Cleanup UDP socket on destruction"""
        if self.udp_socket:
            self.udp_socket.close()
        
def main(args=None):
    rclpy.init(args=args)
    node = CarTelNode()

    # Use MultiThreadedExecutor for concurrent callbacks
    from rclpy.executors import MultiThreadedExecutor
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
