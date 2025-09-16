import sys
from PyQt5.QtWidgets import QDockWidget, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QDialog
from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QPixmap
import datetime
import os
import signal

class RosbagGUI(QDialog):
    def __init__(self):
        super().__init__()
        print('checking')
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.init_ui()
        self.process = QProcess(self)

    def init_ui(self):
        print("Initializing UI...")
        self.setWindowTitle('ROS Bag Tool GUI')
        layout = QVBoxLayout()
        color_dict = {'common': '#c4fcef', 
                      'bag_analysis': '#00c9a7', 
                      'bag_record': '#dd3366', 
                      'N/A':'#BDBDBD'}
        # Path Input
        self.path_label = QLabel('Rosbag Path:')
        self.path_label.setStyleSheet('font-size:16px;')
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path_input = QLineEdit(f'ros_bag/{now}')
        self.path_input.setStyleSheet('font-size:16px;')

        # Path Input and Button in One Line
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.path_input)
        self.btn_update_time = QPushButton('Update Time')
        self.btn_update_time.setStyleSheet(f"font-size:16px; min-width:120px; min-height:50px; background-color:{color_dict['bag_record']}; color:black;")
        self.btn_update_time.clicked.connect(self.update_path_time)
        path_layout.addWidget(self.btn_update_time)
        layout.addLayout(path_layout)

        # Button Area
        btn_style = 'font-size:16px; min-width:200px; min-height:80px;'
        na_style = f"font-size:16px; min-width:200px; min-height:80px; background-color:{color_dict['N/A']}; color:#333;"

        # first row
        btn_row1 = QHBoxLayout()
        self.btn_print_topics = QPushButton('Run print_ros2_topics.sh')
        self.btn_print_topics.setStyleSheet(btn_style + f"background-color:{color_dict['common']}; color:black;")
        self.btn_print_topics.clicked.connect(self.run_print_topics)
        btn_row1.addWidget(self.btn_print_topics)

        self.btn_rqt = QPushButton('RQT')
        self.btn_rqt.setStyleSheet(btn_style + f"background-color:{color_dict['common']}; color:black;")
        self.btn_rqt.clicked.connect(self.run_rqt)
        btn_row1.addWidget(self.btn_rqt)

        self.btn_rqt_graph = QPushButton('RQT Graph')
        self.btn_rqt_graph.setStyleSheet(btn_style + f"background-color:{color_dict['common']}; color:black;")
        self.btn_rqt_graph.clicked.connect(self.run_rqt_graph)
        btn_row1.addWidget(self.btn_rqt_graph)

        self.btn_record = QPushButton('Run rosbag_record.sh')
        self.btn_record.setStyleSheet(btn_style + f"background-color:{color_dict['bag_record']}; color:black;")
        self.btn_record.clicked.connect(self.run_rosbag_record)
        btn_row1.addWidget(self.btn_record)

        layout.addLayout(btn_row1)

        # second row
        btn_row2 = QHBoxLayout()
        self.btn_bag_time = QPushButton('Run bag_time_info.sh')
        self.btn_bag_time.setStyleSheet(btn_style + f"background-color:{color_dict['bag_analysis']}; color:black;")
        self.btn_bag_time.clicked.connect(self.run_bag_time_info)
        btn_row2.addWidget(self.btn_bag_time)

        self.btn_play = QPushButton('Run play_rosbag.sh')
        self.btn_play.setStyleSheet(btn_style + f"background-color:{color_dict['bag_analysis']}; color:black;")
        self.btn_play.clicked.connect(self.run_play_rosbag)
        btn_row2.addWidget(self.btn_play)

        # self.btn_resample_node = QPushButton('Run Resample Node') # to add run_resample_node
        # self.btn_resample_node.setStyleSheet(btn_style + f"background-color:{color_dict['bag_analysis']}; color:black;")
        # self.btn_resample_node.clicked.connect(self.run_resample_node)
        # btn_row2.addWidget(self.btn_resample_node)

        self.btn_play = QPushButton('N/A')
        self.btn_play.setStyleSheet(na_style)
        btn_row2.addWidget(self.btn_play)

        self.btn_play = QPushButton('N/A')
        self.btn_play.setStyleSheet(na_style)
        btn_row2.addWidget(self.btn_play)

        layout.addLayout(btn_row2)

        # Output Area
        self.output_label = QLabel('Output Pad:')
        self.output_label.setStyleSheet('font-size:16px;')
        self.output_text = QLabel('')
        self.output_text.setStyleSheet('QLabel {background: #e0ffff; padding: 5px; font-size:16px; min-width:1000px; max-width:1000px; min-height:300px; max-height:300px; qproperty-alignment: AlignTop;}')
        self.output_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.output_text.setTextInteractionFlags(self.output_text.textInteractionFlags() | Qt.TextSelectableByMouse)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

        
    def update_path_time(self):
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.path_input.setText(f'ros_bag/{now}')

    def run_script(self, script_name, extra_info=''):
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stdout)
        self.process.finished.connect(self.process_finished)
        self.output_text.setText(f'[Run]: {script_name} ... \n')

        script_name = os.path.join(self.base_dir, f'../shell/{script_name}.sh')
        self.process.start('bash', [script_name, extra_info])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.output_text.setText(self.output_text.text() + data)

    def process_finished(self):
        self.output_text.setText(self.output_text.text() + '\n------------------------------------------------[Success]------------------------------------------------')

    def run_rqt(self):
        self.output_text.setText('[Run]: rqt ...\\n')
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stdout)
        self.process.finished.connect(self.process_finished)
        self.process.start('rqt')

    def run_rqt_graph(self):
        self.output_text.setText('[Run]: rqt_graph ...\\n')
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stdout)
        self.process.finished.connect(self.process_finished)
        self.process.start('rqt_graph')
    
    def run_rosbag_record(self):
        if os.path.exists(self.path_input.text().strip()):
            QMessageBox.warning(self, 'Warning', f'Path "{self.path_input.text().strip()}" already exists! Please choose a different path.')
            return
        self.run_script('rosbag_record', extra_info=self.path_input.text())

    def run_print_topics(self):
        self.run_script('print_ros2_topics')

    def run_bag_time_info(self):
        self.run_script('bag_time_info', extra_info=self.path_input.text())

    def run_play_rosbag(self):
        self.run_script('play_rosbag', extra_info=self.path_input.text())

    def run_resample_node(self):
        self.run_script('start_resample_node', extra_info=self.path_input.text())

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    gui = RosbagGUI()
    gui.show()  # 确保调用了 show() 方法
    sys.exit(app.exec_())
