bash CAN_config.sh

# 判断目录是否存在
if [ -d "$HOME/A2RL/AutoVerse" ]; then
	cd "$HOME/A2RL/AutoVerse/autoverse-linux/Linux"
else
	cd "$HOME/A2RL/autoverse/autoverse-linux/Linux"
fi

./Autoverse.sh

# 注意ROS_DOMAIN_ID的设置，系统与仿真保持一致
# 仿真器修改"/autoverse-linux/Linux/Autoverse/Saved/Objects/Eav24_default.json"
# 系统在～/.bashrc中添加export ROS_DOMAIN_ID=823

# Attention: whenever you change the ROS_DOMAIN_ID, be sure to restart the Docker container   
# (using make stop && make start), since the environment variable iss passed through the make start process