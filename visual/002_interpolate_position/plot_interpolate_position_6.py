import numpy as np
import pyvista as pv
import time
from motion.trajectory import interpolate_position, interpolate_position_by_length, polyline_length, cumulative_lengths

# -------------------------
# Функция для визуализации
# -------------------------
def animate_trajectory(trajectory, steps=100):
    cum_lengths = cumulative_lengths(trajectory)
    total_length = polyline_length(trajectory)

    plotter = pv.Plotter(window_size=(800, 600))
    plotter.set_background("black")
    plotter.add_lines(trajectory, color="yellow", width=3)

    sphere_idx = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")
    sphere_len = plotter.add_mesh(pv.Sphere(radius=0.1), color="blue")

    plotter.show(interactive_update=True)

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
            time.sleep(0.03)

        time.sleep(1.0)  # пауза перед повтором

# -------------------------
# Неравномерная траектория
# -------------------------
trajectory_nonuniform = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

print("Неравномерная траектория (красный по индексу, синий по длине)")
animate_trajectory(trajectory_nonuniform)

# -------------------------
# Равномерная траектория
# -------------------------
trajectory_uniform = np.column_stack([
    np.linspace(0, 3, 6),
    np.linspace(0, 3, 6),
    np.linspace(0, 0, 6)
])

print("Равномерная траектория (оба метода одинаково)")
animate_trajectory(trajectory_uniform)
