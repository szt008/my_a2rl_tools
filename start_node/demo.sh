#!/bin/bash
docker exec  kinetiz_alp_qual_stack chmod +x /scripts/start/start_car_gui.sh
docker exec  kinetiz_alp_qual_stack chmod +x /scripts/start/start_car_tel.sh

# Open Terminator
terminator &
sleep 1
xdotool type --delay 1 --clearmodifiers 'docker exec  -w /ros_ws -it kinetiz_alp_qual_stack /scripts/start/start_car_tel.sh'
sleep 1
xdotool key ctrl+shift+e
sleep 1
xdotool type --delay 1 --clearmodifiers 'docker exec  -w /ros_ws -it kinetiz_alp_qual_stack /scripts/start/start_car_gui.sh'
sleep 1
xdotool key ctrl+shift+o
sleep 1
xdotool type --delay 1 --clearmodifiers 'docker exec  -w /ros_ws -it kinetiz_alp_qual_stack /scripts/start/start_control.sh'
xdotool key Return