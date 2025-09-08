source /opt/ros/humble/setup.sh
source ~/A2RL/kinetiz-a2rl/install/setup.bash

if [ ! -d ./ros_bag ]; then
	mkdir ./ros_bag
fi
gnome-terminal -- bash -c "ros2 bag record -a -o ./ros_bag/$(date +%Y%m%d_%H%M%S); exec bash"
