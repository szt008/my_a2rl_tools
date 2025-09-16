killall ros2 # 关闭所有ros节点
sudo pkill -f str2str # 进一步强制清理
tmux kill-server # 关闭tmux会话，一般执行两次弹出下面信息确定关闭
no server running on /tmp/tmux-1000/default

完成关闭动作后可以使用
ps -a
查看是否还有相关的线程残留
