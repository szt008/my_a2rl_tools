###流程：###
1. 采集仿真bag --> ok
2. 加速回放shell --> 回到legion pro7上操作
3. resample节点以得到时间对齐数据 --> 
4. post-process程序

###数据采集内容，按照功能划分并按照从简单到复杂排序###
for Envelope Generation:
    核心变量:
        vehicle state -> 012 order pos （到达加速度层）
        其中a_x a_y a_yaw最为主要，v_x a_z在以往的工作中作为索引
    评价指标:
        tracking Error (侧纵横摆)
        轮胎力、滑移滑转（是否极限）
        其他：轮胎温度（可以用来建立到摩擦系数的映射）

for IL:
    state:
        vehicle state -> 012 order pos （到达加速度层）
        course state -> curvatures, left widths, right widths
        NPC state -> 周车位置速度，非交互工况则无内容
    action: 
        throttle braking steering (actuator layer)
        X Y yaw (motion layer) 用接下来一段时序序列构成 ML planner 输出

for RL:
    state: same as IL | next state: 需要长度为n的存储队列
    action: same as IL
    reward: 
        划分为单车以及多车进行讨论
        单车测速：
            速度（赛道进度）
            稳定性
        多车交互：
            安全性
        注意需要进行归1化提升稳定性
    
    
综合以上内容，可以先将所有内容resample后，进行post-extract获得RL、IL、Envelope Generation需要的数据

GUI设计
需要集成的功能：
topic rqt rqt_graph
rosbag_record rosbag_info rosbag_replay
run_resample_node

接下来开发 resample_node，信息可以一站式参考CarTel msg采集数据的代码

20250912
以下commit cherry pick后再提交
commit 7b3a60a8f17f75393cde02936ecc89d2e192a4fb (HEAD -> dev/dynparam_automan_logo, origin/dev/dynparam_automan_logo)
Author: szt008 <66050801@qq.com>
Date:   Fri Sep 12 14:29:26 2025 +0400

    Automan logo cutouot and add logo to dynparam window

以下命令可以快速将配置文件更新，可以加到GNUmakefile中
param:
	cp -r src/ads_launch/param/* install/ads_launch/share/ads_launch/param/

计划是先resample node提交一次，再ros tool提交一次

两个更新内容：
1.Ali代码关于msg type的更新

import sys, time, numpy as np, os
from typing import Set
from PyQt5.QtWidgets import (
    QDialog, QMainWindow, QDockWidget, QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QAction, QFormLayout, QSpinBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap

# Import DataHandler from the actual module
try:
    from ..data_handler import DataHandler
except ImportError:
    # Add parent directory to path for standalone execution
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from data_handler import DataHandler


按钮模板
class TelemPanel(QDialog):
    _instance = None  # 用于存储单例实例

    def __init__(self):
        super().__init__()
        self.data_handler = DataHandler()

        # 设置窗口标题和大小
        self.setWindowTitle("Telemetry Panel")
        self.setGeometry(100, 100, 400, 300)

        # 创建主布局
        layout = QVBoxLayout()

        # 添加其他控件（如果有）
        # ...

        # 添加图片到布局的下方
        self.image_label = QLabel(self)
        pixmap = QPixmap("src/car_gui/car_gui/lib/automan_lab.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # 图片居中显示
        layout.addWidget(self.image_label)

        # 设置主布局
        self.setLayout(layout)

    @classmethod
    def open_dialog(cls):
        """ Shows Telemetry Panel"""
        if cls._instance is None or not cls._instance.isVisible():
            cls._instance = cls()
        cls._instance.show()
