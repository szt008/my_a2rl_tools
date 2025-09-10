source /opt/ros/humble/setup.sh
source ~/A2RL/kinetiz-a2rl/install/setup.bash

# 读取命令行参数作为存储文件名
BAG_PATH="$1"
if [ -z "$BAG_PATH" ]; then
	BAG_PATH="./ros_bag/$(date +%Y%m%d_%H%M%S)"
fi

DIR=$(dirname "$BAG_PATH")
if [ ! -d "$DIR" ]; then
	mkdir -p "$DIR"
fi

gnome-terminal -- bash -c "ros2 bag record -a -o '$BAG_PATH'; exec bash"
echo "[rosbag_record] Bag will be stored at: $BAG_PATH"

# 如果制定了文件名参数，则使用该参数，否则使用时间作为文件名
# BAG_PATH=${1:-./ros_bag/$(date +%Y%m%d_%H%M%S)}