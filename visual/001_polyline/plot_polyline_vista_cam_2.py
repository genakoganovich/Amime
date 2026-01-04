import pyvista as pv
import numpy as np
import time
from motion.trajectory import polyline_length, cumulative_lengths
import matplotlib.pyplot as plt

# -------------------------
# Траектория
# -------------------------
t = np.linspace(0, 2 * np.pi, 50)
trajectory = np.column_stack([
    np.cos(t),
    np.sin(t),
    t * 0.1
])

cum_lengths = cumulative_lengths(trajectory)
total_length = polyline_length(trajectory)

# -------------------------
# Настройка двух сцен
# -------------------------
# 1. Камера стоит, видит всю траекторию
plotter_static = pv.Plotter(window_size=(600, 500))
plotter_static.set_background("black")
plotter_static.add_lines(trajectory, color="yellow", width=3)
for i in range(len(trajectory) - 1):
    seg = trajectory[i:i + 2]
    color_val = cum_lengths[i] / total_length
    color_rgb = plt.cm.viridis(color_val)[:3]
    plotter_static.add_lines(seg, color=color_rgb, width=5)
plotter_static.add_points(trajectory[1:], color="blue", point_size=8)
sphere_static = plotter_static.add_mesh(pv.Sphere(radius=0.08), color="red")

# 2. Камера следует за шаром
plotter_follow = pv.Plotter(window_size=(600, 500))
plotter_follow.set_background("black")
plotter_follow.add_lines(trajectory, color="yellow", width=3)
for i in range(len(trajectory) - 1):
    seg = trajectory[i:i + 2]
    color_val = cum_lengths[i] / total_length
    color_rgb = plt.cm.viridis(color_val)[:3]
    plotter_follow.add_lines(seg, color=color_rgb, width=5)
plotter_follow.add_points(trajectory[1:], color="blue", point_size=8)
sphere_follow = plotter_follow.add_mesh(pv.Sphere(radius=0.08), color="red")
camera_offset = np.array([0, -1.0, 0.3])

# -------------------------
# Показываем оба окна в интерактивном режиме
# -------------------------
plotter_static.show(interactive_update=True)
plotter_follow.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
for pos in trajectory:
    # обновляем шары
    sphere_static.SetPosition(pos)
    sphere_follow.SetPosition(pos)

    # камера во втором окне следует за шаром
    cam_pos = pos + camera_offset
    plotter_follow.camera_position = [cam_pos.tolist(), pos.tolist(), [0, 0, 1]]

    # обновление сцен
    plotter_static.update()
    plotter_follow.update()

    time.sleep(0.05)
