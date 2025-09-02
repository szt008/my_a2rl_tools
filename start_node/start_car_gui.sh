#!/bin/bash

# Start terminator and split terminals to run commands
source /opt/ros/humble/setup.sh
cd /ros_ws/
source /ros_ws/install/setup.sh

ros2 run car_gui car_gui_node