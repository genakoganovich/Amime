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
# Сцена PyVista
# -------------------------
plotter = pv.Plotter()
plotter.set_background("black")

# траектория
plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3,
)

# шар
sphere = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="red",
)

# стрелка 1 — interpolate_orientation (дискретная)
arrow_seg = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="blue",
)

# стрелка 2 — interpolate_orientation_by_length (по длине)
arrow_len = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="green",
)

arrow_seg.SetPosition(TRAJECTORY[0])
arrow_len.SetPosition(TRAJECTORY[0])

last_dir_seg = directions[0].copy()
last_dir_len = np.array([1.0, 0.0, 0.0])

plotter.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
while True:
    for i in range(STEPS):
        s = i * total_length / (STEPS - 1)

        pos = interpolate_position_by_length(TRAJECTORY, s)
        sphere.SetPosition(pos)

        # ---------- 1. interpolate_orientation ----------
        seg_idx = np.searchsorted(cum_lengths, s, side="right") - 1
        seg_idx = np.clip(seg_idx, 0, len(directions) - 1)
        dir_seg = directions[seg_idx]

        if not np.allclose(dir_seg, last_dir_seg):
            yaw = np.degrees(np.arctan2(dir_seg[1], dir_seg[0]))
            arrow_seg.SetOrientation(0.0, 0.0, yaw)
            last_dir_seg = dir_seg.copy()

        arrow_seg.SetPosition(pos)

        # ---------- 2. interpolate_orientation_by_length ----------
        dir_len = interpolate_orientation_by_length(
            cum_lengths,
            directions[:-1],
            s,
        )

        if not np.allclose(dir_len, last_dir_len):
            yaw = np.degrees(np.arctan2(dir_len[1], dir_len[0]))
            arrow_len.SetOrientation(0.0, 0.0, yaw)
            last_dir_len = dir_len.copy()

        arrow_len.SetPosition(pos)

        plotter.update()
        time.sleep(FRAME_DELAY)

    time.sleep(PAUSE_END)
