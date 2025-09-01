已经启动仿真器和main，但是提示CAN没有接通

已经收集了**ros2 param list**的terminal反馈，包含参数服务器所有动态参数，见[text](<ros2 param list.md>)
其中节点按照模块进行划分：

感知（Perception）：
/eav24/perception_node

决策（Prediction/Decision）：
/eav24/prediction_node
/eav24/race_control_node（部分决策/竞赛控制）

定位（Localization）：
/eav24/state_estimation_node

规划（Planning）：
/eav24/eav24/graph_trajectory_rviz_node（轨迹可视化）
/eav24/eav24/trajectory_chunk_extended_rviz_node
/eav24/eav24/trajectoryv2rviz_node
/eav24/map_ar_reader_node（地图相关，部分规划）

控制（Control）：
/eav24/motion_control_node

使用以下命令可以将服务器上的参数保存下来，可以用于看看参数是否修改成功
ros2 param dump [节点名] > [./参数文件名.yaml]
例如：
ros2 param dump /eav24/motion_control_node > param_demo.yaml

下一步通过写在car_tel中的定时程序进行参数更改，每隔几秒加1