import pyvista as pv
import numpy as np
import time

from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
    interpolate_position,
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
)

from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
    STEPS,
    FRAME_DELAY,
    )


# -------------------------
# Данные
# -------------------------
cum_len = cumulative_lengths(TRAJECTORY)
total_len = polyline_length(TRAJECTORY)
directions_seg = interpolate_orientation(TRAJECTORY)

# -------------------------
# Сцена
# -------------------------
plotter = pv.Plotter()
plotter.set_background("black")

plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3
)

# --- Первый шар: interpolate_position + interpolate_orientation
sphere_seg = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS), color="red")
arrow_seg = plotter.add_mesh(pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE), color="red")

# --- Второй шар: interpolate_position_by_length + interpolate_orientation_by_length
sphere_len = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS), color="cyan")
arrow_len = plotter.add_mesh(pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE), color="cyan")

plotter.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
while True:
    for i in range(STEPS):
        # Параметр и длина
        t = i / (STEPS - 1)
        s = t * total_len

        # ------------------------------------------------
        # 1) interpolate_position (индексная интерполяция)
        # ------------------------------------------------
        pos_seg = interpolate_position(TRAJECTORY, t * (len(TRAJECTORY) - 1))

        # находим сегмент
        seg_idx = int(np.clip(int((t * (len(TRAJECTORY) - 1))), 0, len(directions_seg) - 1))
        dir_seg = directions_seg[seg_idx]

        sphere_seg.SetPosition(pos_seg)
        arrow_seg.SetPosition(pos_seg)
        yaw_seg = np.degrees(np.arctan2(dir_seg[1], dir_seg[0]))
        arrow_seg.SetOrientation(0, 0, yaw_seg)

        # ------------------------------------------------
        # 2) interpolate_position_by_length (по длине)
        # ------------------------------------------------
        pos_len = interpolate_position_by_length(TRAJECTORY, s)
        dir_len = interpolate_orientation_by_length(cum_len, directions_seg[:-1], s)

        sphere_len.SetPosition(pos_len)
        arrow_len.SetPosition(pos_len)
        yaw_len = np.degrees(np.arctan2(dir_len[1], dir_len[0]))
        arrow_len.SetOrientation(0, 0, yaw_len)

        # обновление сцены
        plotter.update()
        time.sleep(FRAME_DELAY)