使用以下命令查看UDP端口的信号
nc -ul 6672
其中6672是端口号
nc -ul 6672与目前的car_gui互斥，只有一个可以显示信号

sudo iftop
可以查看为网络负载信息(htop类似)，使用前进行安装：
sudo apt install iftop
使用tailscale组成的局域网查看：
sudo iftop -i tailscale0 # -i 指需要输入端口
使用q推出
