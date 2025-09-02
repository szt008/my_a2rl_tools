#!/bin/bash
set -e

# Source ROS 2 Environment
source /opt/ros/humble/setup.bash
source ~/A2RL/kinetiz-a2rl/install/setup.bash

# Get timestamp and create output folder
TIME=$(date +%Y%m%d_%H%M%S)
DIR="./param_data/param_$TIME"
mkdir -p "$DIR"

# Get all node names 获取所有节点名（用空格分隔字符串或用数组）
NODES=(/eav24/lqr_control_node /eav24/trajserver_node)

# Loop through nodes and export parameters
for NODE in "${NODES[@]}"; do
    # Remove leading slash and replace with _ for filename 去除前导斜杠作为文件名
    FILENAME=$(echo $NODE | sed 's#^/##;s#/#_#g')
    ros2 param dump $NODE > "$DIR/${FILENAME}.yaml"
    echo "save $NODE parameters to ${FILENAME}.yaml"
done

echo "All the param files are saved into $DIR."

# This script exports parameters of specified ROS 2 nodes and saves them as YAML files for later viewing and use.
# 该文件的功能为导出指定ROS 2节点的参数，并将其保存为YAML文件，方便后续查看和使用。