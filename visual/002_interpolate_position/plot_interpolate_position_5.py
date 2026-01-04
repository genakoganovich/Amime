import numpy as np
import pyvista as pv
import time
from motion.trajectory import (cumulative_lengths, polyline_length,
                               interpolate_position, interpolate_position_by_length)

# -------------------------
# Траектория
# -------------------------
trajectory = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

# -------------------------
# Вычисляем длины
# -------------------------
cum_lengths = cumulative_lengths(trajectory)
total_length = polyline_length(trajectory)

# -------------------------
# Настройка PyVista
# -------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# Траектория — желтая
plotter.add_lines(trajectory, color="yellow", width=3)

# Красный шар (камера на стержне)
sphere_idx = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")
# Синий шар для сравнения движения по длине
sphere_len = plotter.add_mesh(pv.Sphere(radius=0.1), color="blue")

plotter.show(interactive_update=True)

# -------------------------
# Длина стержня
# -------------------------
length_rod = 1.0
rod_actor = None

# -------------------------
# Анимация
# -------------------------
steps = 100
pause_time = 1.0

while True:
    for i in range(steps):
        # --- позиции шаров ---
        t_idx = i * (len(trajectory) - 1) / (steps - 1)
        pos_idx = interpolate_position(trajectory, t_idx)
        sphere_idx.SetPosition(pos_idx)

        s_len = i * total_length / (steps - 1)
        pos_len = interpolate_position_by_length(trajectory, s_len)
        sphere_len.SetPosition(pos_len)

        # --- вычисляем направление движения ---
        # если не последний шаг, берем следующую точку, иначе предыдущую
        if i < steps - 1:
            next_pos = interpolate_position(trajectory, (i+1)*(len(trajectory)-1)/(steps-1))
            dir_rod = next_pos - pos_idx
        else:
            prev_pos = interpolate_position(trajectory, (i-1)*(len(trajectory)-1)/(steps-1))
            dir_rod = pos_idx - prev_pos

        dir_rod = dir_rod / np.linalg.norm(dir_rod)  # нормализация
        rod_end = pos_idx + dir_rod * length_rod  # конец стержня

        # --- камера на стержне ---
        plotter.camera_position = [rod_end.tolist(), pos_idx.tolist(), [0, 0, 1]]

        # --- визуализация стержня ---
        if rod_actor is not None:
            plotter.remove_actor(rod_actor)
        rod_actor = plotter.add_lines(np.array([pos_idx, rod_end]), color="white", width=2)

        # --- обновление сцены ---
        plotter.update()
        time.sleep(0.05)

    time.sleep(pause_time)
