import numpy as np
from numba import njit
import matplotlib.pyplot as plt

def get_tyre_forces(tan_sy, sx, Fz_all, p):
    sy = np.arctan(tan_sy)
    sx = np.clip(sx, -1, 1)
    S = np.sqrt(sy**2 + sx**2)
    sy_S = sy/np.maximum(S, 0.0001)
    sx_S = sx/np.maximum(S, 0.0001)

    Byf = np.tan(np.pi/(2*p['tyre_Cyf']))/p['tyre_sy_peak_f']
    Byr = np.tan(np.pi/(2*p['tyre_Cyr']))/p['tyre_sy_peak_r']
    Bxf = np.tan(np.pi/(2*p['tyre_Cxf']))/p['tyre_sx_peak_f']
    Bxr = np.tan(np.pi/(2*p['tyre_Cxr']))/p['tyre_sx_peak_r']

    # Fz_load = np.zeros(4)
    # Fz_load[0:2] = np.clip(Fz_all[0:2], p['tyre_Fznom_f']/3, p['tyre_Fznom_f']*3)
    # Fz_load[2:4] = np.clip(Fz_all[2:4], p['tyre_Fznom_r']/3, p['tyre_Fznom_r']*3)

    # Dy_effective_f = p['tyre_Dyf'] + p['Dy2f'] * (FzLoad - p['tyre_Fznom_f']) / p['tyre_Fznom_f'];

    Fyf = Fz_all[0:2] * sy_S[0:2] * p['tyre_Dyf'] * np.sin( p['tyre_Cyf'] * np.arctan( Byf*S[0:2]) )
    Fyr = Fz_all[2:4] * sy_S[2:4] * p['tyre_Dyr'] * np.sin( p['tyre_Cyr'] * np.arctan( Byr*S[2:4]) )

    Fxf = Fz_all[0:2] * sx_S[0:2] * p['tyre_Dxf'] * np.sin( p['tyre_Cxf'] * np.arctan( Bxf*S[0:2]) )
    Fxr = Fz_all[2:4] * sx_S[2:4] * p['tyre_Dxr'] * np.sin( p['tyre_Cxr'] * np.arctan( Bxr*S[2:4]) )

    Fx = np.zeros(4)
    Fx[0:2] = Fxf
    Fx[2:4] = Fxr
    Fy = np.zeros(4)
    Fy[0:2] = Fyf
    Fy[2:4] = Fyr

    return Fx, Fy

def main():
    vehicle_param = {}
    vehicle_param['m'] = 740
    vehicle_param['lf'] = 1.75
    vehicle_param['lr'] = 1.35
    vehicle_param['t'] = 0.9
    vehicle_param['g'] = 9.81

    Fz_front = vehicle_param['m'] * vehicle_param['g'] * vehicle_param['lr'] / (vehicle_param['lf'] + vehicle_param['lr'])
    Fz_rear = vehicle_param['m'] * vehicle_param['g'] * vehicle_param['lf'] / (vehicle_param['lf'] + vehicle_param['lr'])

    Fz_static = np.array([Fz_front/2, Fz_front/2, Fz_rear/2, Fz_rear/2])
    print(Fz_static)

    tire_param = {}
    tire_param['tyre_Cyf'] = 1.5
    tire_param['tyre_Cyr'] = 1.6
    tire_param['tyre_Cxf'] = 1.3
    tire_param['tyre_Cxr'] = 1.4

    tire_param['tyre_Dyf'] = 1.5
    tire_param['tyre_Dyr'] = 1.55
    tire_param['tyre_Dxf'] = 1.4
    tire_param['tyre_Dxr'] = 1.7

    tire_param['tyre_sy_peak_f'] = 0.08725
    tire_param['tyre_sy_peak_r'] = 0.078525
    tire_param['tyre_sx_peak_f'] = 0.07
    tire_param['tyre_sx_peak_r'] = 0.06

    sx_range = np.linspace(-0.1, 0.1, 50)
    sy_range = np.linspace(-5/180 * 3.14, 5/180 * 3.14, 50)
    SX, SY = np.meshgrid(sx_range, sy_range)

    Fx_all = np.zeros((4, SX.shape[0], SX.shape[1]))
    Fy_all = np.zeros((4, SX.shape[0], SX.shape[1]))
    Fxy_all = np.zeros((4, SX.shape[0], SX.shape[1]))

    for i in range(SX.shape[0]):
        for j in range(SX.shape[1]):
            tan_sy = np.array([np.tan(SY[i, j])] * 4)
            sx = np.array([SX[i, j]] * 4)
            Fx, Fy = get_tyre_forces(tan_sy, sx, Fz_static, tire_param)
            Fx_all[:, i, j] = Fx
            Fy_all[:, i, j] = Fy
            Fxy_all[:, i, j] = np.sqrt(Fy**2 + Fx**2)

    # 3D surface plot
    fig = plt.figure(figsize=(16, 12))
    titles = ['Front Left', 'Front Right', 'Rear Left', 'Rear Right']
    for k in range(4):
        ax = fig.add_subplot(2, 2, k+1, projection='3d')
        surf = ax.plot_surface(SX, SY, Fxy_all[k], cmap='viridis', edgecolor='none')
        ax.set_title(f'{titles[k]}: |Fxy|')
        ax.set_xlabel('sx')
        ax.set_ylabel('sy')
        ax.set_zlabel('Force')
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

        num_theta = 100
        num_r = 100
        theta_list = np.linspace(-np.pi, np.pi, num_theta)
        r_max = np.sqrt(np.max(sx_range)**2 + np.max(sy_range)**2)
        max_sx = []
        max_sy = []
        max_fxy = []
        angle_list = []
        for theta in theta_list:
            r_list = np.linspace(0, r_max, num_r)
            fxy_r = []
            sx_r = []
            sy_r = []
            fx_r = []
            fy_r = []
            for r in r_list:
                sx = r * np.cos(theta)
                sy = r * np.sin(theta)
                tan_sy = np.array([np.tan(sy)] * 4)
                sx_arr = np.array([sx] * 4)
                Fx, Fy = get_tyre_forces(tan_sy, sx_arr, Fz_static, tire_param)
                fxy = np.sqrt(Fx[k]**2 + Fy[k]**2)
                fxy_r.append(fxy)
                sx_r.append(sx)
                sy_r.append(sy)
                fx_r.append(Fx[k])
                fy_r.append(Fy[k])
            idx = np.argmax(fxy_r)
            max_sx.append(sx_r[idx])
            max_sy.append(sy_r[idx])
            max_fxy.append(fxy_r[idx])
            # 计算夹角
            input_vec = np.array([sx_r[idx], sy_r[idx]])
            force_vec = np.array([fx_r[idx], fy_r[idx]])
            if np.linalg.norm(input_vec) > 1e-6 and np.linalg.norm(force_vec) > 1e-6:
                cos_angle = np.dot(input_vec, force_vec) / (np.linalg.norm(input_vec) * np.linalg.norm(force_vec))
                angle = np.arccos(np.clip(cos_angle, -1, 1)) * 180 / 3.14  # 弧度
            else:
                angle = 0
            angle_list.append(angle)

        # 用颜色表示夹角（偏移），用scatter画在地面
        # sc = ax.plot(max_sx, max_sy, np.zeros_like(max_fxy), c='#F17582', linewidth=5, label='Angle(Fxy/Input)')
        sc = ax.plot(max_sx, max_sy, max_fxy, c='#F17582', linewidth=5, zorder=10)
        ax.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()