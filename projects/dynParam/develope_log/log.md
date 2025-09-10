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