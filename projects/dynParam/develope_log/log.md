将目前的话题、参数、类型、数值、指示灯集成为widget，名命为DynParamWidget

根据yaml生成gui，主要就是读取话题、参数、类型、数值

在亚斯码头红房调试，使用以下命令安装tailscale以建立虚拟局域网
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up # 启动
tailscale status # 查看虚拟局域网状态，输出会列出所有与你同属一个 Tailnet 的设备（包括主机名、IP、在线状态等），你和谁组网一目了然。

<!-- Tailscale 的虚拟局域网是基于你的 Tailscale 账户（如 Google、GitHub、Microsoft 登录）自动建立的。 -->

Ali 成功让车载电脑的car_tel发送本车信息到笔记本的car_gui, 两端的IP填写的都是笔记本的IP(Tailscale虚拟局域网)

注意：在测试前车端需要开始CAN，make start-CAN
还需要测试 UDP DynParam 是否有效 -> 可以发送到 car_tel,但是还无法收到 car_tel 的回信

100.68.86.3     automan-vector-16    kinetiz_racing@ linux 
100.89.100.65   a2rl                 kinetiz_racing@ linux 

20250910 morning
目前有两个事情，一个是需要动态配置IP，另一项是需要查清onboard无法动态配置参数的原因
需要动态配置的IP：
    car_tel:
        1. 用于发送本车信息 指定端口 6672
        所处函数：def send_udp_data(self, msg)
        real: 远端笔记本IP（开启Tailscale后的 100.68.86.3）
        sim: 笔记本闭环IP（无需开启Tailscale 127.0.0.1）也就是发给自己

        car_tel_node.py Line 180 
        self.udp_socket.sendto(serialized_data, (self.udp_host, self.udp_port))

        2. UDP listener用于接收动态参数信息 指定端口 6671
        所处函数：def __init__(self):
        real: 车载电脑IP（开启Tailscale后的 100.89.100.65）
        sim: 笔记本闭环IP（无需开启Tailscale 127.0.0.1）

        car_tel_node.py Line 88 
        self.udp_socket.bind((self.udp_host, self.udp_port))

        3. 用于返回动态参数确定消息 指定端口 6673
        所处函数：def listen_udp_data(self):
        real: 远端笔记本IP（开启Tailscale后的 100.68.86.3）
        sim: 笔记本闭环IP（无需开启Tailscale 127.0.0.1）也就是发给自己

        car_tel_node.py Line 245 
        self.udp_socket.sendto(serialized_data, (self.udp_host, self.udp_port))
        ack_addr = ('100.89.100.65', 10000) # Force the port number to be set to 10000.
        self.udp_socket.sendto(ack_bytes, ack_addr) 
    
    car_gui:
        1. 用于接收UDP车辆状态信息 指定端口 6672
        所处函数：def setup_udp_receiver(self):
        real: 远端笔记本IP（开启Tailscale后的 100.68.86.3）
        sim: 笔记本闭环IP（无需开启Tailscale 127.0.0.1）也就是发给自己

        car_gui_node.py Line 54 
        self.udp_socket.bind((self.udp_host, self.udp_port))

        2.发送动态参数 指定端口 6671
        所处函数：def send_udp(self):
        real: 车载IP（开启Tailscale后的 100.89.100.65）
        sim: 笔记本闭环IP（无需开启Tailscale 127.0.0.1）也就是发给自己

        udp_param_dialog.py line 220
        sock.sendto(msg, ('100.89.100.65', 9999))

        3.接收动态参数返回信号 指定端口 6673
        所处函数：def listen_feedback(self):
        real: 远端笔记本IP（开启Tailscale后的 100.68.86.3）
        sim: 笔记本闭环IP（无需开启Tailscale 127.0.0.1）也就是发给自己

        udp_param_dialog.py line 220
        sock.bind(('100.68.86.3', 10000))

完成了通过yaml自动配置，快速的IP切换。目前在笔记本上运行正常，但是在车上param server有些问题。
param server的问题可能是DDS或者docker造成的

在车上调试使用tmux模式，tmux模式的关闭命令，一般要重复两次弹出提示文本确定关闭
tmux kill-server
tmux ls可以看状态
    