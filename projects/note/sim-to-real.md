## sim param
```
lqr_control_node:
  ros__parameters:
    dt: 0.01
    input_timeout_sec: 0.4
    lat_e_max: 2.0
    heading_err_max: 0.25
    force_recovery: False
    fr_lat_e_max: 10.0
    fr_heading_err_max: 0.7
    safe_stop_brake: 15.0
    emergency_stop_brake: 29.0
    traj_preview_size: 200
    max_steer: 0.32423756 #20.2/62.3 # radian in shaft/ratio: max st_rad
    max_throttle_low_speed: 60.0
    max_throttle: 100.0
    max_throttle_speed_thr: 20.0
    max_brake: 60.0
    race_control_decel: 8.0 # m/s^2
    hard_stop_decel: 10.0 # m/s^2
    hard_stop_decel_V2: 0.001 # *V^2
    max_st_rate: 0.3490658504 # 20deg
    max_throttle_rate: 85.0 # /sec
    max_brake_rate: 80.0 # /sec
    Cd0: 0.7 # 1.0 for real car
    Cd1: 0.0
    Cd2: 0.001
    Ct0: -2.41368000e+03
    Ct1: 1.46747703e+00
    Ct2: -2.25393420e-04
    Ct3: 1.08662626e-08
    min_vel_slip_control: 15.0
    slip_control_mode: 2
    TC_enabled: True
    brake_bias: 0.58
    min_vx_fb: -12.0 # NEGATIVE
    syf_max: 7.0
    beta_ref_mult: 1.0
    beta_gain: 0.0
    engine_map_mult: 0.9
    power_based_map: False
    enable_help_steer_br: False
    brake2pressure: 120000.0 # 12000000/100 # 100 cmd to max Pa
    pressure2torque: 0.0004 #3600/12000000 #
    pressure2torque_hightemp: 0.0004 #3600/12000000 #
    steer2actuator_rad: 0.194 #20.2/100 # 100 cmd to max_steer of actuator
    steer_ratio: 62.3 # st_rad 2 act_rad
    steer_offset_rad: 0.0
    kp_vx: 1.0
    kp_vx_max: 2.0 # 6.66 ? 
    kp_sx: 0.5
    m: 750
    R: 0.307
    fdr: 2.818
    gear_ratios: [0.0, 3.083, 2.286, 1.7647, 1.421, 1.19, 1.036 ]
    
                      #13   22    27    33    66   None
                      #1-2  2-3   3-4   4-5   5-6  None
    up_rpms:      [0, 4200, 6800, 6800, 6800, 6900, 9999]

                      #11   16.1  24    30    62 
               #None  #2-1  3-2   4-3   5-4   6-5
    down_rpms: [0, 0, 2550, 4200, 4500, 4800, 5700]

    lat_err_sat: 3.0
    dec_lookup_name: "/slip_lookup/vx_ax_sx.pkl"
    acc_lookup_name: "/slip_lookup/vx_ax_sx6_gas.pkl"
    recording_path: "/trajectories/recording_yas_north_56p0.json"
    joystick_guard: False
    use_act_lqr: True
    vx_dependent_cfcr: True
    tau: 0.03 # LQR act 1/10
    num_delay: 4 # steer sample
    lf: 1.733
    lr: 1.3817
    tf: 0.75
    tr: 0.75 

trajserver_node:
  ros__parameters:
    dt: 0.01
    p2p_always_active: False
    input_timeout_sec: 0.4
    pit_speed: 7.0
    time_adv_ax: 0.05
    time_adv_vx: 0.05
    time_adv_vx_vec: [1, 10, 20, 40, 60, 80]
    time_adv_vec: [0.12, 0.12, 0.12, 0.12, 0.12, 0.12]
    preview_size_dt: 200
    preview_size_ds: 200

    gg_acc_mult: [0.0, 0.0, 0.0,  0.0,  0.0, 0.0, 0.0] # gg mult ile toplaniyor
    gg_dec_mult: [0.05, 0.0, 0.0, 0.15, 0.0, 0.0, 0.0]

    #              0    1     2      3        4     5            6     
    gg_mult:    [1.12,  0.98,  0.98,   1.13,   1.05,  1.10,     1.15]
    corner_idx: [3300, 5300,  7500  ,13500,   25300, 26100,     27100]

    Cd0: 0.7
    Cd1: 0.0
    Cd2: 0.001

    ggv: 0.0015      # +v^2
    ggv_acc: 0.0015  # +v^2
    ggv_dec: 0.0017  # +v^2
    
    ax_max: 6.5
    dec_max: 10.0
    acc_max_lat: 14.5
    combined_coef: 1.5
    # lap_based_mult: [1.0]
    lap_based_mult:   [1.0, 1.0, 1.0, 1.0,]
    lap_based_v_max : [80.0, 80.0, 80.0, 80.0]
    target_lap_time: 60.0
    trajectory_paths: [
      "/trajectories/opt_traj_50_yas_north_bnds_v15_with_pit.json",
      "/trajectories/opt_traj_50_yas_north_bnds_v15_with_pit.json",
      "/trajectories/opt_traj_50_yas_north_bnds_v15_with_pit.json",
      "/trajectories/opt_traj_50_yas_north_bnds_v17_with_pit.json",

    ]
    p2p_index: [14300, 28300]
    pit_stop_index: 29274
    disable_p2p: True
    enable_wall_tracker: False
    brake_warmup_mode: False
    brake_warmup_activation_speed: 40.0
    brake_warmup_target_speed: 17.0
    brake_warmup_max_lap: 2
    manual_traj_switch_mode: False
    current_traj_override: 0

rb_planner_node:
  ros__parameters:
    input_timeout_sec: 0.2
    opponent_timeout_sec: 1.0
    lat0: 24.46992202098782
    lon0: 54.60522506805341
    y_offset: 0.0
    x_offset: 0.0
    traj_path: "/trajectories/opt_traj_3_5_yas_north_bnds_v2_with_pit.json"
    recording_path: "/trajectories/recording_yas_north_56p0.json"
    oppo_source: "lidar"
```

## real param
```
lqr_control_node:
  ros__parameters:
    dt: 0.01
    input_timeout_sec: 0.4
    lat_e_max: 2.0
    heading_err_max: 0.25
    force_recovery: False
    fr_lat_e_max: 5.0
    fr_heading_err_max: 0.5
    safe_stop_brake: 20.0
    emergency_stop_brake: 29.0
    traj_preview_size: 200
    max_steer: 0.32423756 #20.2/62.3 # radian in shaft/ratio: max st_rad at wheel
    max_throttle_low_speed: 60.0
    max_throttle: 100.0
    max_throttle_speed_thr: 20.0
    max_brake: 60.0
    race_control_decel: 8.0 # m/s^2
    hard_stop_decel: 10.0 # m/s^2
    hard_stop_decel_V2: 0.002 # *V^2
    max_st_rate: 0.3490658504 # 20deg
    max_throttle_rate: 85.0 # /sec
    max_brake_rate: 80.0 # /sec
    Cd0: 0.8 # 1.0 for real car
    Cd1: 0.0
    Cd2: 0.001
    Ct0: -2.41368000e+03
    Ct1: 1.46747703e+00
    Ct2: -2.25393420e-04
    Ct3: 1.08662626e-08
    min_vel_slip_control: 15.0
    slip_control_mode: 2
    TC_enabled: True
    brake_bias: 0.57
    min_vx_fb: -12.0 # NEGATIVE
    syf_max: 7.0
    beta_ref_mult: 0.0
    beta_gain: 0.0
    engine_map_mult: 0.7
    power_based_map: False
    enable_help_steer_br: False
    brake2pressure: 120000.0 # 12000000/100 # 100 cmd to max Pa
    pressure2torque: 0.00025 #3600/12000000 #
    pressure2torque_hightemp: 0.00037 #3600/12000000 #
    steer2actuator_rad: 0.194 #19.4/100 # 100 cmd to max_steer of actuator
    steer_ratio: 62.3 # st_rad 2 act_rad
    steer_offset_rad: 0.0
    kp_vx: 1.0
    kp_vx_max: 2.0 # 6.66 ? 
    kp_sx: 0.5
    m: 750
    R: 0.307
    fdr: 2.818
    gear_ratios: [0.0, 3.083, 2.286, 1.7647, 1.421, 1.19, 1.036 ]
    
                      #13   22    27    33    66   None
                      #1-2  2-3   3-4   4-5   5-6  None
    #up_rpms:      [0, 4200, 6800, 6800, 6800, 6900, 9999]
    up_rpms:      [0, 4200, 6900, 6900, 7050, 7000, 9999]

                      #11   16.1  24    30    62 
               #None  #2-1  3-2   4-3   5-4   6-5
    down_rpms: [0, 0, 2550, 4200, 4500, 4800, 5700]

    lat_err_sat: 3.0
    dec_lookup_name: "/slip_lookup/vx_ax_sx.pkl"
    acc_lookup_name: "/slip_lookup/vx_ax_sx6_gas.pkl"
    recording_path: "/trajectories/recording_yas_north_56p0.json"
    joystick_guard: False
    use_act_lqr: True
    vx_dependent_cfcr: True
    tau: 0.03 # LQR act 1/10
    num_delay: 4 # steer sample
    lf: 1.733
    lr: 1.3817
    tf: 0.75
    tr: 0.75 
    
trajserver_node:
  ros__parameters:
    dt: 0.01
    p2p_always_active: False
    input_timeout_sec: 0.4
    pit_speed: 6.5
    time_adv_ax: 0.05
    time_adv_vx: 0.05
    time_adv_vx_vec: [1, 10, 20, 40, 60, 80]
    time_adv_vec: [0.12, 0.12, 0.12, 0.12, 0.12, 0.12]
    preview_size_dt: 200
    preview_size_ds: 200

    gg_acc_mult: [0.0, 0.0, 0.0,  0.0,  0.0, 0.0, 0.0] # gg mult ile toplaniyor
    gg_dec_mult: [0.0, 0.0, 0.0, 0.05,  -0.05, 0.0, 0.0]

    #              0    1     2      3        4     5            6     
    gg_mult:    [1.18, 1.08,  1.10,  1.13,    1.11,  1.14,     1.18]
    corner_idx: [3300, 5300,  7500  ,13500,   25300, 26100,     27100]

    Cd0: 0.8
    Cd1: 0.0
    Cd2: 0.001

    ggv: 0.0016      # +v^2
    ggv_acc: 0.0015  # +v^2
    ggv_dec: 0.0015  # +v^2
    
    ax_max: 6.5
    dec_max: 10.0
    acc_max_lat: 15.2
    combined_coef: 1.7
    lap_based_mult:   [0.77, 0.85, 0.90, 0.95, 0.99,  1.015, 1.025, 1.04, 1.055,   1.065, 1.075, 1.085]
    lap_based_v_max : [70.0, 80.0, 80.0, 80.0, 80.0,  80.0, 80.0, 80.0, 80.0,   80.0, 80.0, 80.0]
    target_lap_time: 59.5
    trajectory_paths: [
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",

      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",

      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
      "/trajectories/opt_traj_52_yas_north_bnds_v18_with_pit.json",
    ]
    p2p_index: [14300, 28300]
    pit_stop_index: 29270 # 99999 #= Dont stop
    disable_p2p: False
    enable_wall_tracker: False
    brake_warmup_mode: False
    brake_warmup_activation_speed: 40.0
    brake_warmup_target_speed: 17.0
    brake_warmup_max_lap: 2
    manual_traj_switch_mode: False
    current_traj_override: 0


rb_planner_node:
  ros__parameters:
    input_timeout_sec: 0.2
    opponent_timeout_sec: 1.0
    lat0: 24.46992202098782
    lon0: 54.60522506805341
    y_offset: 0.0
    x_offset: 0.0
    traj_path: "/trajectories/opt_traj_3_5_yas_north_bnds_v2_with_pit.json"
    recording_path: "/trajectories/recording_yas_north_56p0.json"
    oppo_source: "virtual" # PAY ATTENTION THIS CONFIG
```