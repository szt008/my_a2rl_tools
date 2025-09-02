# conda activate avrs
cd ~/A2RL/kinetiz-a2rl

killall ros2 

source /opt/ros/humble/setup.sh
source ~/A2RL/kinetiz-a2rl/install/setup.bash

make start
bash start_simulation_alp.sh
