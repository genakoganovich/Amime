import pyvista as pv
import numpy as np
import time
from motion.trajectory import cumulative_lengths, polyline_length, interpolate_position_by_length, interpolate_orientation

# -------------------------
# Пример неравномерной траектории
# -------------------------
trajectory = np.array([
    [0,0,0],
    [0.5,0,0],
    [2,0,0],
    [2,1,0],
    [3,1,0],
    [3,3,0]
])

# -------------------------
# Вычисляем длины и направления
# -------------------------
cum_lengths = cumulative_lengths(trajectory)
total_length = polyline_length(trajectory)
directions = interpolate_orientation(trajectory)

# -------------------------
# Настройка сцены PyVista
# -------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# траектория
plotter.add_mesh(pv.lines_from_points(trajectory), color="yellow", line_width=3)

# красный шар
sphere_actor = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")

# стрелка направления
arrow_actor = plotter.add_mesh(pv.Arrow(direction=directions[0], scale=0.3), color="blue")

plotter.show(interactive_update=True)

# -------------------------
# Анимация бесконечно
# -------------------------
steps = 200
while True:
    for i in range(steps):
        # движение по длине траектории равномерно
        s_len = i * total_length / (steps - 1)
        pos = interpolate_position_by_length(trajectory, s_len)

        # находим ближайший сегмент для направления
        d_idx = np.argmin(np.linalg.norm(trajectory - pos, axis=1))
        dir_vec = directions[d_idx]

        # обновляем шар и стрелку
        sphere_actor.SetPosition(pos)
        arrow_actor.SetPosition(pos)
        angle = np.degrees(np.arctan2(dir_vec[1], dir_vec[0]))
        arrow_actor.SetOrientation(angle, 0, 0)

        plotter.update()
        time.sleep(0.03)

    # пауза в конце траектории
    time.sleep(1.0)
