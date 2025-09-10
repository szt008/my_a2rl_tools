###流程：###
1. 采集仿真bag --> ok
2. 加速回放shell --> 回到legion pro7上操作
3. resample节点以得到时间对齐数据 --> 
4. post-process程序

###数据采集内容，按照功能划分并按照从简单到复杂排序###
for Envelope Generation:
    核心变量:
        vehicle state -> 012 order pos （到达加速度层）
        其中a_x a_y a_yaw最为主要，v_x a_z在以往的工作中作为索引
    评价指标:
        tracking Error (侧纵横摆)
        轮胎力、滑移滑转（是否极限）
        其他：轮胎温度（可以用来建立到摩擦系数的映射）

for IL:
    state:
        vehicle state -> 012 order pos （到达加速度层）
        course state -> curvatures, left widths, right widths
        NPC state -> 周车位置速度，非交互工况则无内容
    action: 
        throttle braking steering (actuator layer)
        X Y yaw (motion layer) 用接下来一段时序序列构成 ML planner 输出

for RL:
    state: same as IL | next state: 需要长度为n的存储队列
    action: same as IL
    reward: 
        划分为单车以及多车进行讨论
        单车测速：
            速度（赛道进度）
            稳定性
        多车交互：
            安全性
        注意需要进行归1化提升稳定性
    
    
综合以上内容，可以先将所有内容resample后，进行post-extract获得RL、IL、Envelope Generation需要的数据

GUI设计
需要集成的功能：
topic rqt rqt_graph
rosbag_record rosbag_info rosbag_replay
run_resample_node

接下来开发 resample_node，信息可以一站式参考CarTel msg采集数据的代码