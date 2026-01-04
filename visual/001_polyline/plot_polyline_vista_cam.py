import pyvista as pv
import numpy as np
import time
from motion.trajectory import polyline_length, cumulative_lengths
import matplotlib.pyplot as plt  # для colormap

# -------------------------
# Создаем траекторию
# -------------------------
t = np.linspace(0, 2 * np.pi, 50)
trajectory = np.column_stack([
    np.cos(t),
    np.sin(t),
    t * 0.1
])

# -------------------------
# Вычисляем сегменты и кумулятивные длины
# -------------------------
cum_lengths = cumulative_lengths(trajectory)  # [0, l1, l2, ...]
total_length = polyline_length(trajectory)

# -------------------------
# Настройка сцены
# -------------------------
plotter = pv.Plotter(window_size=(900, 700))
plotter.set_background("black")

# вся траектория желтым
plotter.add_lines(trajectory, color="yellow", width=3)

# добавляем сегменты с градиентом по длине
for i in range(len(trajectory) - 1):
    seg = trajectory[i:i + 2]
    color_val = cum_lengths[i] / total_length  # от 0 до 1
    color_rgb = plt.cm.viridis(color_val)[:3]  # RGB 0..1
    plotter.add_lines(seg, color=color_rgb, width=5)

# точки на концах сегментов (кумулятивная длина)
plotter.add_points(trajectory[1:], color="blue", point_size=8)

# шар
sphere_actor = plotter.add_mesh(pv.Sphere(radius=0.08), color="red")

# -------------------------
# Камера смещена за шаром
# -------------------------
camera_offset = np.array([0, -1.0, 0.3])

plotter.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
for pos in trajectory:
    # обновляем шар
    sphere_actor.SetPosition(pos)

    # камера следует за шаром
    cam_pos = pos + camera_offset
    plotter.camera_position = [cam_pos.tolist(), pos.tolist(), [0, 0, 1]]

    plotter.update()
    time.sleep(0.05)
