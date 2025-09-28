class KalmanLPF1D:
    """
    1D 卡尔曼低通（随机游走模型）:
        x_k = x_{k-1} + w,   w ~ N(0, Q)
        z_k = x_k       + v, v ~ N(0, R)
    适合把标量测量 z_k 平滑成低噪声、低滞后的估计 x_hat。
    """
    def __init__(self, x0=0.0, P0=1.0, Q=1e-3, R=1e-2):
        self.x = float(x0)   # 状态(即我们要的低通输出)
        self.P = float(P0)   # 协方差
        self.Q = float(Q)    # 过程噪声方差(越大越“跟”测量，平滑更弱、滞后更小)
        self.R = float(R)    # 测量噪声方差(越大越不信测量，更平滑、滞后更大)

    def reset(self, x0=0.0, P0=1.0):
        self.x = float(x0)
        self.P = float(P0)

    def update(self, z):
        # 预测（随机游走：x^- = x）
        x_pred = self.x
        P_pred = self.P + self.Q

        # 更新
        K = P_pred / (P_pred + self.R)      # 卡尔曼增益 (0~1)
        self.x = x_pred + K * (z - x_pred)  # 后验估计
        self.P = (1.0 - K) * P_pred

        return self.x
