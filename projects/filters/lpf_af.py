import numpy as np
from collections import deque

def alpha_from_fc(fc, Ts):
    """
    根据截止频率 fc(Hz) 和采样周期 Ts(s) 计算一阶低通的 alpha
    推导自: alpha = Ts / (Ts + tau), tau = 1/(2*pi*fc)
    """
    tau = 1.0 / (2.0 * np.pi * fc)
    return Ts / (Ts + tau)

class FirstOrderLowPassFilter:
    def __init__(self, tau=None, Ts=None, alpha=None, y0=0.0):
        """
        一阶低通滤波器（支持用 tau+Ts 或直接给 alpha 初始化）
        - 若提供 alpha：直接使用 alpha
        - 否则使用 tau 和 Ts 计算 alpha = Ts / (tau + Ts)
        """
        if alpha is None:
            if tau is None or Ts is None:
                raise ValueError("Either provide alpha, or provide (tau and Ts).")
            alpha = Ts / (tau + Ts)
        if not (0.0 < alpha < 1.0):
            raise ValueError("alpha must be in (0,1).")
        self.alpha = float(alpha)
        self.y = float(y0)

    def reset(self, y0=0.0):
        self.y = float(y0)

    def update(self, x):
        self.y = self.alpha * x + (1.0 - self.alpha) * self.y
        return self.y


class MovingAverageFilter:
    def __init__(self, window_size=5, init=None):
        """
        简单滑动均值滤波器
        - window_size: 窗口长度（样本数）
        - init: 可选的初始填充值（用于启动阶段避免偏小均值）
        """
        if window_size <= 0:
            raise ValueError("window_size must be positive.")
        self.window_size = int(window_size)
        self.buffer = deque(maxlen=self.window_size)
        if init is not None:
            for _ in range(self.window_size):
                self.buffer.append(float(init))

    def reset(self, init=None):
        self.buffer = deque(maxlen=self.window_size)
        if init is not None:
            for _ in range(self.window_size):
                self.buffer.append(float(init))

    def update(self, x):
        self.buffer.append(float(x))
        return float(np.mean(self.buffer))


class HybridLPFMeanFilter:
    def __init__(self, tau=None, Ts=None, alpha=None, window_size=5, y0=0.0):
        """
        低通 + 均值 混合滤波器
        执行顺序：先一阶低通，再滑动均值
        """
        self.lpf = FirstOrderLowPassFilter(tau=tau, Ts=Ts, alpha=alpha, y0=y0)
        self.mean = MovingAverageFilter(window_size=window_size, init=y0)

    def reset(self, y0=0.0):
        self.lpf.reset(y0)
        self.mean.reset(y0)

    def update(self, x):
        y_lpf = self.lpf.update(x)
        y_out = self.mean.update(y_lpf)
        return y_out


# ====== 示例用法 ======
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # 生成测试信号：低频正弦 + 白噪声 + 两个尖峰
    T = 5.0
    N = 500
    t = np.linspace(0, T, N)
    Ts = t[1] - t[0]
    x = np.sin(2*np.pi*1.0*t) + 0.3*np.random.randn(N)
    x[100] += 5.0
    x[300] -= 4.0

    # 参数设置：用目标截止频率 fc 计算 alpha（等价于用 tau）
    fc = 2.0             # 目标截止频率(Hz)，可根据需求调整
    alpha = alpha_from_fc(fc, Ts)

    # 构造滤波器
    lpf_only = FirstOrderLowPassFilter(alpha=alpha, y0=0.0)
    hybrid = HybridLPFMeanFilter(alpha=alpha, window_size=7, y0=0.0)

    # 在线处理
    y_lpf = [lpf_only.update(xi) for xi in x]
    y_hybrid = [hybrid.update(xi) for xi in x]

    # 画图
    plt.figure(figsize=(10,6))
    plt.plot(t, x, label="Original Signal", alpha=0.6)
    plt.plot(t, y_lpf, label="Low-pass Filter", linewidth=2)
    plt.plot(t, y_hybrid, label="Hybrid (Low-pass + Moving Average)", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Low-pass + Moving Average (Hybrid) Filtering")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
