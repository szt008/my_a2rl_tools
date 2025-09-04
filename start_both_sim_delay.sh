#!/bin/bash

# 在第一个终端运行 start_avrs_simulator.sh
gnome-terminal -- bash -c "bash ./start_avrs_simulator.sh; exec bash"

# 等待10秒
sleep 10

# 在第二个终端运行 start_kinetiz_main.sh
gnome-terminal -- bash -c "bash ./start_kinetiz_main.sh; exec bash"
