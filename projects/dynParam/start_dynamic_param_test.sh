#!/bin/bash

# No.1 终端运行 start_avrs_simulator.sh
gnome-terminal -- bash -c "bash ./start_avrs_simulator.sh; exec bash"

# No.2 终端运行 start_kinetiz_main.sh
bash ./start_kinetiz_main.sh

# No.3 终端运行 car_tel (需要make start进入docker)
docker exec  -w /ros_ws -it kinetiz_alp_qual_stack /scripts/start/start_car_tel.sh

# No.4 终端运行 udp_gui
python src/car_gui/dynamic_param_gui/UDP_dynParam_multi-param.py

# No.5 启动录制（可选）
