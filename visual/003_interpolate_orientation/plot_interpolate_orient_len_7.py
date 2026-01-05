import pyvista as pv
import numpy as np
import time
from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
)

# -------------------------
# Конфигурация
# -------------------------
TRAJECTORY = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

ARROW_SCALE = 0.4
SPHERE_RADIUS = 0.1
STEPS = 150
FRAME_DELAY = 0.03
PAUSE_END = 1.0

# -------------------------
# Подготовка данных
# -------------------------
directions = interpolate_orientation(TRAJECTORY)
cum_lengths = cumulative_lengths(TRAJECTORY)
total_length = polyline_length(TRAJECTORY)

# -------------------------
# PyVista сцена
# -------------------------
plotter = pv.Plotter()
plotter.set_background("black")

plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3,
)

sphere_actor = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="red",
)

# стрелка вдоль X
arrow_actor = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="blue",
)

arrow_actor.SetPosition(TRAJECTORY[0])
last_direction = np.array([1.0, 0.0, 0.0])

plotter.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
while True:
    for i in range(STEPS):
        s = i * total_length / (STEPS - 1)

        pos = interpolate_position_by_length(TRAJECTORY, s)
        direction = interpolate_orientation_by_length(
            cum_lengths,
            directions[:-1],
            s,
        )

        sphere_actor.SetPosition(pos)

        # --- абсолютный поворот вокруг Z ---
        if not np.allclose(direction, last_direction):
            yaw = np.degrees(np.arctan2(direction[1], direction[0]))
            arrow_actor.SetOrientation(0.0, 0.0, yaw)
            last_direction = direction.copy()

        arrow_actor.SetPosition(pos)

        plotter.update()
        time.sleep(FRAME_DELAY)

    time.sleep(PAUSE_END)
