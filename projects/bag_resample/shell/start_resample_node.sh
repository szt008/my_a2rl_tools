echo 'Resample Node Started'

source /opt/ros/humble/setup.sh
source ~/A2RL/kinetiz-a2rl/install/setup.bash

gnome-terminal -- bash -c "docker exec kinetiz_alp_qual_stack chmod +x /scripts/start/start_resample.sh; 
docker exec  -w /ros_ws -it kinetiz_alp_qual_stack /scripts/start/start_resample.sh; exec bash"
