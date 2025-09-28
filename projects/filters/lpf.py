class FirstOrderLowPassFilter:
    def __init__(self, tau, Ts, y0=0.0):
        """
        First-order low-pass filter
        tau : time constant
        Ts  : sampling period
        y0  : initial output
        """
        self.tau = tau
        self.Ts = Ts
        self.alpha = Ts / (tau + Ts)
        self.y = y0

    def update(self, x):
        """
        Input x, return filtered output y
        """
        self.y = self.alpha * x + (1 - self.alpha) * self.y
        return self.y


# ===== Example usage =====
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # Simulated input signal: low-frequency sine + high-frequency noise
    t = np.linspace(0, 5, 500)
    x = np.sin(2*np.pi*1*t) + 0.5*np.sin(2*np.pi*20*t)

    # Create filter
    tau = 0.1   # time constant
    Ts = t[1]-t[0]  # sampling period
    lp_filter = FirstOrderLowPassFilter(tau, Ts)

    # Filtering
    y = [lp_filter.update(xi) for xi in x]

    # Plot
    plt.plot(t, x, label="Original signal")
    plt.plot(t, y, label="Filtered signal", linewidth=2)
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("First-order Low-pass Filter Example")
    plt.show()