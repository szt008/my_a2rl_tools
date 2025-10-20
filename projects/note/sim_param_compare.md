## SIM vs REAL parameter comparison

Below are side-by-side comparison tables for the nodes defined in `projects/note/sim-to-real.md`.

### How to read
- Column `sim` shows parameters used in simulation.
- Column `real` shows parameters used on the real car.
- Column `diff` indicates whether the values differ (YES = different).

---

### lqr_control_node

| Parameter | sim | real | diff |
|---|---:|---:|---:|
| dt | 0.01 | 0.01 | |
| input_timeout_sec | 0.4 | 0.4 | |
| lat_e_max | 2.0 | 2.0 | |
| heading_err_max | 0.25 | 0.25 | |
| force_recovery | False | False | |
| fr_lat_e_max | 10.0 | 5.0 | YES |
| fr_heading_err_max | 0.7 | 0.5 | YES |
| safe_stop_brake | 15.0 | 20.0 | YES |
| emergency_stop_brake | 29.0 | 29.0 | |
| traj_preview_size | 200 | 200 | |
| max_steer | 0.32423756 | 0.32423756 | |
| max_throttle_low_speed | 60.0 | 60.0 | |
| max_throttle | 100.0 | 100.0 | |
| max_throttle_speed_thr | 20.0 | 20.0 | |
| max_brake | 60.0 | 60.0 | |
| race_control_decel | 8.0 | 8.0 | |
| hard_stop_decel | 10.0 | 10.0 | |
| hard_stop_decel_V2 | 0.001 | 0.002 | YES |
| max_st_rate | 0.3490658504 | 0.3490658504 | |
| max_throttle_rate | 85.0 | 85.0 | |
| max_brake_rate | 80.0 | 80.0 | |
| Cd0 | 0.7 | 0.8 | YES |
| Cd1 | 0.0 | 0.0 | |
| Cd2 | 0.001 | 0.001 | |
| Ct0 | -2413.68 | -2413.68 | |
| Ct1 | 1.46747703 | 1.46747703 | |
| Ct2 | -0.00022539342 | -0.00022539342 | |
| Ct3 | 1.08662626e-08 | 1.08662626e-08 | |
| min_vel_slip_control | 15.0 | 15.0 | |
| slip_control_mode | 2 | 2 | |
| TC_enabled | True | True | |
| brake_bias | 0.58 | 0.57 | YES |
| min_vx_fb | -12.0 | -12.0 | |
| syf_max | 7.0 | 7.0 | |
| beta_ref_mult | 1.0 | 0.0 | YES |
| beta_gain | 0.0 | 0.0 | |
| engine_map_mult | 0.9 | 0.7 | YES |
| power_based_map | False | False | |
| enable_help_steer_br | False | False | |
| brake2pressure | 120000.0 | 120000.0 | |
| pressure2torque | 0.0004 | 0.00025 | YES |
| pressure2torque_hightemp | 0.0004 | 0.00037 | YES |
| steer2actuator_rad | 0.194 | 0.194 | |
| steer_ratio | 62.3 | 62.3 | |
| steer_offset_rad | 0.0 | 0.0 | |
| kp_vx | 1.0 | 1.0 | |
| kp_vx_max | 2.0 | 2.0 | |
| kp_sx | 0.5 | 0.5 | |
| m | 750 | 750 | |
| R | 0.307 | 0.307 | |
| fdr | 2.818 | 2.818 | |
| gear_ratios | [0.0, 3.083, 2.286, 1.7647, 1.421, 1.19, 1.036] | [0.0, 3.083, 2.286, 1.7647, 1.421, 1.19, 1.036] | |
| up_rpms | [0, 4200, 6800, 6800, 6800, 6900, 9999] | [0, 4200, 6900, 6900, 7050, 7000, 9999] | YES |
| down_rpms | [0, 0, 2550, 4200, 4500, 4800, 5700] | [0, 0, 2550, 4200, 4500, 4800, 5700] | |
| lat_err_sat | 3.0 | 3.0 | |
| dec_lookup_name | "/slip_lookup/vx_ax_sx.pkl" | "/slip_lookup/vx_ax_sx.pkl" | |
| acc_lookup_name | "/slip_lookup/vx_ax_sx6_gas.pkl" | "/slip_lookup/vx_ax_sx6_gas.pkl" | |
| recording_path | "/trajectories/recording_yas_north_56p0.json" | "/trajectories/recording_yas_north_56p0.json" | |
| joystick_guard | False | False | |
| use_act_lqr | True | True | |
| vx_dependent_cfcr | True | True | |
| tau | 0.03 | 0.03 | |
| num_delay | 4 | 4 | |
| lf | 1.733 | 1.733 | |
| lr | 1.3817 | 1.3817 | |
| tf | 0.75 | 0.75 | |
| tr | 0.75 | 0.75 | |

---

### trajserver_node

| Parameter | sim | real | diff |
|---|---:|---:|---:|
| dt | 0.01 | 0.01 | |
| p2p_always_active | False | False | |
| input_timeout_sec | 0.4 | 0.4 | |
| pit_speed | 7.0 | 6.5 | YES |
| time_adv_ax | 0.05 | 0.05 | |
| time_adv_vx | 0.05 | 0.05 | |
| time_adv_vx_vec | [1,10,20,40,60,80] | [1,10,20,40,60,80] | |
| time_adv_vec | [0.12,0.12,0.12,0.12,0.12,0.12] | [0.12,0.12,0.12,0.12,0.12,0.12] | |
| preview_size_dt | 200 | 200 | |
| preview_size_ds | 200 | 200 | |
| gg_acc_mult | [0,0,0,0,0,0,0] | [0,0,0,0,0,0,0] | |
| gg_dec_mult | [0.05,0,0,0.15,0,0,0] | [0.0,0.0,0.0,0.05,-0.05,0.0,0.0] | YES |
| gg_mult | [1.12,0.98,0.98,1.13,1.05,1.10,1.15] | [1.18,1.08,1.10,1.13,1.11,1.14,1.18] | YES |
| corner_idx | [3300,5300,7500,13500,25300,26100,27100] | [3300,5300,7500,13500,25300,26100,27100] | |
| Cd0 | 0.7 | 0.8 | YES |
| Cd1 | 0.0 | 0.0 | |
| Cd2 | 0.001 | 0.001 | |
| ggv | 0.0015 | 0.0016 | YES |
| ggv_acc | 0.0015 | 0.0015 | |
| ggv_dec | 0.0017 | 0.0015 | YES |
| ax_max | 6.5 | 6.5 | |
| dec_max | 10.0 | 10.0 | |
| acc_max_lat | 14.5 | 15.2 | YES |
| combined_coef | 1.5 | 1.7 | YES |
| lap_based_mult | [1.0,1.0,1.0,1.0] | [0.77,0.85,0.90,0.95,0.99,1.015,1.025,1.04,1.055,1.065,1.075,1.085] | YES |
| lap_based_v_max | [80,80,80,80] | [70,80,80,80,80,80,80,80,80,80,80,80] | YES |
| target_lap_time | 60.0 | 59.5 | YES |
| trajectory_paths | (different files) | (different files) | YES |
| p2p_index | [14300,28300] | [14300,28300] | |
| pit_stop_index | 29274 | 29270 | YES |
| disable_p2p | True | False | YES |
| enable_wall_tracker | False | False | |
| brake_warmup_mode | False | False | |
| brake_warmup_activation_speed | 40.0 | 40.0 | |
| brake_warmup_target_speed | 17.0 | 17.0 | |
| brake_warmup_max_lap | 2 | 2 | |
| manual_traj_switch_mode | False | False | |
| current_traj_override | 0 | 0 | |

---

### rb_planner_node

| Parameter | sim | real | diff |
|---|---:|---:|---:|
| input_timeout_sec | 0.2 | 0.2 | |
| opponent_timeout_sec | 1.0 | 1.0 | |
| lat0 | 24.46992202098782 | 24.46992202098782 | |
| lon0 | 54.60522506805341 | 54.60522506805341 | |
| y_offset | 0.0 | 0.0 | |
| x_offset | 0.0 | 0.0 | |
| traj_path | "/trajectories/opt_traj_3_5_yas_north_bnds_v2_with_pit.json" | "/trajectories/opt_traj_3_5_yas_north_bnds_v2_with_pit.json" | |
| recording_path | "/trajectories/recording_yas_north_56p0.json" | "/trajectories/recording_yas_north_56p0.json" | |
| oppo_source | "lidar" | "virtual" | YES |

---

### Notes
- I added a `diff` column to every table. `YES` marks parameters that differ between sim and real.
- If you want, I can also generate TSV/CSV/XLSX files (one combined or per-node) and add them to the repo for direct download.
