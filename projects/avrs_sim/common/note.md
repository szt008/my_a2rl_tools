1. 使用以下命令进行多车放置
avrs spawn-object

放置 NPC 车辆需要指定地点
目前已有 MvStart0 , MvStart1 , MvStart2 , and MvStart3 几个位置可以使用。可以通过在environment configuration file的lanmarks部分进行定义增加新的位置。
（后续需要开环测试的位置）

eav24_mv0.json和eav24_mv1.json是实例文件，其中specName为指定的位置名称

例如由 eav24_mv0.json 定义的车辆，其中 specName 字段被设置为 eav24_mv0。放置命令是 avrs spawn-object eav24_mv0 MvStart0 。在该命令中，eav24_mv0 指定应使用其 specName 设置为此值的配置文件，并且车辆应在 MvStart0 地标处生成。eav24_mv0.json文件所处位置应该包含在objectTemplatePaths中。 

2. 清楚所有 NPC
avrs vehicle-replay despawn --all

3. 窗口模式
./Autoverse.sh -ResX=640 -ResY=360 -WINDOWED

4. Autoverse如果不依赖于CLI则可以通过网络协议进行通信
   
5. 修改地图
   autoverse-linux/Linux/Autoverse/Saved/simconfig.json
   中的defaultEnvironment进行修改后运行仿真器
   可选的地图包括：
   YasmarinaNorth、YasMarina、Suzuka、Autonodrome

6. 移动本车位置，应该是TP开头的命令