# 20250915 VDA 第一天 #
上午沟通测试和修改安全逻辑
下午开始测试，分为两组实验12:00到18：00

第1组实验（VDA_011）：
无lidar Odometry，无感知信号接入
speed limit: 5m/s->12m/s

修改：
主要内容
- 调整Lqr control model中的刚度参数
- 增加Cd0 Cd2 brake_bias的更新，及动态设置命令用于在测试过程中调整
- 驱动系统 engine_map_mult 2.0->1.0
- 制动系统 pressure2torque 0.000166667->0.00025
次要内容
- 最大油门 max_throttle 15.0->20.0
- 紧急制动减速度20m/s^2->6m/s^2

第2组实验（VDA_012）：
无lidar Odometry，无感知信号接入
speed limit: 5m/s->15m/s

# 20250916 VDA 第二天 #
加入VDA场地激光雷达地图
早8:00-10:00修改定位bug

第1组实验：
GPS和lidar Odometry融合定位，无感知信号接入
speed limit: 5m/s->20m/s