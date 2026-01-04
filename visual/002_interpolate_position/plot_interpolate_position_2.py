import numpy as np
import pyvista as pv
import time
from motion.trajectory import (cumulative_lengths, polyline_length,
                               interpolate_position, interpolate_position_by_length)

# -------------------------
# Неравномерная траектория
# -------------------------
trajectory = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

# Вычисляем длины
cum_lengths = cumulative_lengths(trajectory)
total_length = polyline_length(trajectory)

# -------------------------
# Настройка PyVista
# -------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# Вся траектория — желтая
plotter.add_lines(trajectory, color="yellow", width=3)

# Шары
sphere_idx = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")
sphere_len = plotter.add_mesh(pv.Sphere(radius=0.1), color="blue")

# Активируем интерактивный режим
plotter.show(interactive_update=True)

# -------------------------
# Бесконечная анимация с закрашенной пройденной частью
# -------------------------
steps = 100
pause_time = 1.0  # пауза в конце траектории

while True:
    # ссылки на красные линии (пройденная часть)
    passed_idx_actor = None
    passed_len_actor = None

    for i in range(steps):
        # --- позиции шаров ---
        t_idx = i * (len(trajectory) - 1) / (steps - 1)
        pos_idx = interpolate_position(trajectory, t_idx)
        sphere_idx.SetPosition(pos_idx)

        s_len = i * total_length / (steps - 1)
        pos_len = interpolate_position_by_length(trajectory, s_len)
        sphere_len.SetPosition(pos_len)

        # --- закрашиваем пройденную часть для красного шара ---
        if passed_idx_actor is not None:
            plotter.remove_actor(passed_idx_actor)
        if i > 0:
            passed_seg_idx = np.array([interpolate_position(trajectory, j * (len(trajectory) - 1) / (steps - 1)) for j in range(i+1)])
            mesh_idx = pv.lines_from_points(passed_seg_idx)
            passed_idx_actor = plotter.add_mesh(mesh_idx, color="red", line_width=5)

        # --- закрашиваем пройденную часть для синего шара ---
        if passed_len_actor is not None:
            plotter.remove_actor(passed_len_actor)
        if i > 0:
            passed_seg_len = np.array([interpolate_position_by_length(trajectory, j * total_length / (steps - 1)) for j in range(i+1)])
            mesh_len = pv.lines_from_points(passed_seg_len)
            passed_len_actor = plotter.add_mesh(mesh_len, color="blue", line_width=5)

        # обновляем сцену
        plotter.update()
        time.sleep(0.05)

    # пауза в конце траектории
    time.sleep(pause_time)
