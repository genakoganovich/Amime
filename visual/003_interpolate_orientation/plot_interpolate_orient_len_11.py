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

# -----------------------------------------------------
# Траектория
# -----------------------------------------------------
TRAJECTORY = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

SPHERE_RADIUS = 0.12
ARROW_SCALE = 0.3
STEPS = 150
FRAME_DELAY = 0.03

# -----------------------------------------------------
# Данные
# -----------------------------------------------------
cum_len = cumulative_lengths(TRAJECTORY)
total_len = polyline_length(TRAJECTORY)
directions = interpolate_orientation(TRAJECTORY)

# -----------------------------------------------------
# Сцена с 1 окном и 2 подкадрами (1×2)
# -----------------------------------------------------
plotter = pv.Plotter(shape=(1, 2))
plotter.set_background("black")

# =====================================================
# SUBPLOT 0 — Статичная камера
# =====================================================
plotter.subplot(0, 0)
plotter.add_text("Static camera", font_size=14)

plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3,
)

sphere_actor = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="cyan",
)

arrow_actor = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="cyan",
)

# Камера статичная — просто ставим удобный ракурс
plotter.camera.position = (6, -6, 6)
plotter.camera.focal_point = (1, 1, 0)
plotter.camera.up = (0, 0, 1)

# =====================================================
# SUBPLOT 1 — Камера прицеплена к шару сзади/сверху
# =====================================================
plotter.subplot(0, 1)
plotter.add_text("Follow camera", font_size=14)

plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3,
)

sphere_actor_2 = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="cyan",
)

arrow_actor_2 = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="cyan",
)

# Показываем окно
plotter.show(interactive_update=True)

# -----------------------------------------------------
# АНИМАЦИЯ
# -----------------------------------------------------
while True:
    for i in range(STEPS):
        t = i / (STEPS - 1)
        s = t * total_len

        # Позиция шара
        pos = interpolate_position_by_length(TRAJECTORY, s)

        # Ориентация
        direction = interpolate_orientation_by_length(
            cum_len,
            directions[:-1],
            s
        )
        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        # =========================================================
        # Обновляем левую половину (STATIC CAMERA)
        # =========================================================
        plotter.subplot(0, 0)
        sphere_actor.SetPosition(pos)
        arrow_actor.SetPosition(pos)
        arrow_actor.SetOrientation(0, 0, yaw)

        # =========================================================
        # Обновляем правую половину (FOLLOW CAMERA)
        # =========================================================
        plotter.subplot(0, 1)
        sphere_actor_2.SetPosition(pos)
        arrow_actor_2.SetPosition(pos)
        arrow_actor_2.SetOrientation(0, 0, yaw)

        # Камера идёт за шаром
        # offset = точка, где находится камера относительно шара
        # Например: чуть позади (-direction) и выше (z+1.0)
        cam_offset = -direction * 1.0 + np.array([0, 0, 0.8])
        cam_pos = pos + cam_offset

        plotter.camera.position = cam_pos.tolist()
        plotter.camera.focal_point = pos.tolist()
        plotter.camera.up = (0, 0, 1)

        plotter.update()
        time.sleep(FRAME_DELAY)