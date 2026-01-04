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
plotter.add_lines(trajectory, color="yellow", width=3)

# Шары
sphere_idx = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")
sphere_len = plotter.add_mesh(pv.Sphere(radius=0.1), color="blue")

plotter.show(interactive_update=True)

# -------------------------
# Бесконечная анимация
# -------------------------
steps = 100
pause_time = 1.0  # пауза в конце траектории

while True:
    for i in range(steps):
        # движение по индексу
        t_idx = i * (len(trajectory) - 1) / (steps - 1)
        pos_idx = interpolate_position(trajectory, t_idx)
        sphere_idx.SetPosition(pos_idx)

        # движение по длине
        s_len = i * total_length / (steps - 1)
        pos_len = interpolate_position_by_length(trajectory, s_len)
        sphere_len.SetPosition(pos_len)

        plotter.update()
        time.sleep(0.05)

    # пауза в конце траектории
    time.sleep(pause_time)
