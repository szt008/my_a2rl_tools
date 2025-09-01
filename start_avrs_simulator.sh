bash CAN_config.sh

cd ~/A2RL/AutoVerse/autoverse-linux/Linux
./Autoverse.sh

# 注意ROS_DOMAIN_ID的设置，系统与仿真保持一致
# 仿真器修改"/autoverse-linux/Linux/Autoverse/Saved/Objects/Eav24_default.json"
# 系统在～/.bashrc中添加export ROS_DOMAIN_ID=108

# Attention: whenever you change the ROS_DOMAIN_ID, be sure to restart the Docker container   
# (using make stop && make start), since the environment variable iss passed through the make start process