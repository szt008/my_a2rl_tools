#!/bin/bash
# 仅显示rosbag的Start、End和Duration信息

BAG_DIR="$1"
ros2 bag info "$BAG_DIR" | grep -E '^(Start:|End:|Duration:)'
