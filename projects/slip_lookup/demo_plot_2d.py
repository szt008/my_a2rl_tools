import pickle
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import RegularGridInterpolator
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.gridspec import GridSpec

def load_lookup(filename):
    with open(filename, 'rb') as f:
        interp_obj = pickle.load(f)
    return interp_obj

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ax_lookup_dec (interactive sx)')
        self.ax_lookup_dec = load_lookup('/home/automan/A2RL/my_a2rl_tools/projects/slip_lookup/vx_ax_sx.pkl')
        self.vx_grid = self.ax_lookup_dec.grid[0]
        self.ax_grid = self.ax_lookup_dec.grid[1]
        self.sx_grid = self.ax_lookup_dec.grid[2]
        self.num_vx = 1000
        self.num_ax = 1000
        self.vx_dense = np.linspace(self.vx_grid[0], self.vx_grid[-1], self.num_vx)
        self.ax_dense = np.linspace(self.ax_grid[0], self.ax_grid[-1], self.num_ax)

        # UI
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # matplotlib canvas with GridSpec for cbar
        self.fig = plt.figure(figsize=(8, 6))
        gs = GridSpec(1, 2, width_ratios=[20, 1])
        self.ax = self.fig.add_subplot(gs[0], projection='3d')
        self.cax = self.fig.add_subplot(gs[1])
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas, stretch=10)

        # slider
        slider_layout = QVBoxLayout()
        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(self.sx_grid)-1)
        self.slider.setValue(len(self.sx_grid)//2)
        self.slider.valueChanged.connect(self.update_plot)
        slider_layout.addWidget(QLabel("sx index"))
        slider_layout.addWidget(self.slider)
        self.sx_label = QLabel(f"sx_fixed: {self.sx_grid[self.slider.value()]:.3f}")
        slider_layout.addWidget(self.sx_label)
        layout.addLayout(slider_layout, stretch=1)

        self.cbar = None
        self.update_plot()

    def update_plot(self):
        sx_idx = self.slider.value()
        sx_fixed = self.sx_grid[sx_idx]
        self.sx_label.setText(f"sx_fixed: {sx_fixed:.3f}")

        vx_fixed = 40.0
        ax_vals = self.ax_dense
        points = np.stack([np.full_like(ax_vals, vx_fixed), ax_vals, np.full_like(ax_vals, sx_fixed)], axis=-1)
        Z = self.ax_lookup_dec(points)

        self.ax.clear()
        self.ax.plot(ax_vals, Z, color='blue', linewidth=2)
        self.ax.set_xlabel('ax')
        self.ax.set_ylabel(f'lookup value (vx=40, sx={sx_fixed:.2f})')
        self.ax.set_title('ax_lookup_dec 2D curve')

        self.cax.clear()
        self.cbar = None  # 2D曲线不需要colorbar

        self.canvas.draw()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = PlotWindow()
    win.show()
    sys.exit(app.exec_())