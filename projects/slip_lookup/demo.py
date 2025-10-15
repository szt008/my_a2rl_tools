import pickle
import numpy as np
import matplotlib.pyplot as plt

def load_lookup(filename):
    with open(filename, 'rb') as f:
        T_lookup = pickle.load(f)
    return T_lookup

ax_lookup_dec = load_lookup('projects/slip_lookup/vx_ax_sx.pkl')
ax_lookup_acc = load_lookup('projects/slip_lookup/vx_ax_sx6_gas.pkl')

vx_min, vx_max = 0, 80 # m/s
ax_min, ax_max = -30, 15 # m/s^2

vx_grid = ax_lookup_acc.grid[0]
ax_grid = ax_lookup_acc.grid[1]
sx_grid = ax_lookup_acc.grid[2]

print(vx_grid)
print(ax_grid)
print(sx_grid)

vx_grid = ax_lookup_dec.grid[0]
ax_grid = ax_lookup_dec.grid[1]
sx_grid = ax_lookup_dec.grid[2]

print(vx_grid)
print(ax_grid)
print(sx_grid)

# 固定 sx 的值（例如取第一个或中间值）
sx_fixed = sx_grid[len(sx_grid)//2]

# 构造采样点
VX, AX = np.meshgrid(vx_grid, ax_grid)
print(VX)
print(AX)

points = np.stack([VX.ravel(), AX.ravel(), np.full(VX.size, sx_fixed)], axis=-1)
print(points)
Z = []
for p in points:
    p = tuple(p)
    print(p)
    p = (1.0, 2.0, 3.1)
    print(ax_lookup_acc(p))
    # Z.append()
print(Z)
# self.ax_lookup_accel((curr_vx, ax_ref_tyre*0.7, sx[2]))
# # 绘制曲面
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# surf = ax.plot_surface(VX, AX, Z, cmap='viridis')
# ax.set_xlabel('vx')
# ax.set_ylabel('ax')
# ax.set_zlabel(f'lookup value (sx={sx_fixed:.2f})')
# plt.colorbar(surf)
# plt.title('ax_lookup_acc surface (fixed sx)')
# plt.show()

