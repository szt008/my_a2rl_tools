#!/bin/bash
# 回放指定rosbag目录

BAG_DIR="$1"
# 获取包的总时长
BAG_DURATION=$(ros2 bag info "$BAG_DIR" | grep '^Duration:' | awk '{print $2}')

# 记录回放开始结束时间
gnome-terminal -- bash -c "ros2 bag play "$BAG_DIR" -r 5; exec bash"

echo -e " "
echo -e "Bag duration: $BAG_DURATION"