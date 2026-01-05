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
# Окно с двумя видами
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

# Удобная статичная камера
plotter.camera.position = (6, -6, 6)
plotter.camera.focal_point = (1, 1, 0)
plotter.camera.up = (0, 0, 1)

# =====================================================
# SUBPLOT 1 — Камера прикреплена к основанию стрелки
# =====================================================
plotter.subplot(0, 1)
plotter.add_text("Camera attached to arrow base", font_size=14)

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

plotter.show(interactive_update=True)

# -----------------------------------------------------
# АНИМАЦИЯ
# -----------------------------------------------------
while True:
    for i in range(STEPS):
        t = i / (STEPS - 1)
        s = t * total_len

        # Позиция и ориентация
        pos = interpolate_position_by_length(TRAJECTORY, s)
        direction = interpolate_orientation_by_length(
            cum_len,
            directions[:-1],
            s
        )
        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        # -----------------------------------------
        # ЛЕВОЕ окно (статичная камера)
        # -----------------------------------------
        plotter.subplot(0, 0)
        sphere_actor.SetPosition(pos)
        arrow_actor.SetPosition(pos)
        arrow_actor.SetOrientation(0, 0, yaw)

        # -----------------------------------------
        # ПРАВОЕ окно (камера прикреплена к СТЕЛКЕ)
        # -----------------------------------------
        plotter.subplot(0, 1)
        sphere_actor_2.SetPosition(pos)
        arrow_actor_2.SetPosition(pos)
        arrow_actor_2.SetOrientation(0, 0, yaw)

        # -----------------------------------------------------
        # КАМЕРА ПРИКРЕПЛЕНА К ОСНОВАНИЮ СТРЕЛКИ
        #
        # Требования:
        #   • камера расположена ПОЗАДИ стрелки
        #   • немного выше стрелки
        #   • в кадре должна быть видна сама стрелка
        #
        # pos -----> направление direction -----> движение
        #
        # Камера:
        #   position = pos - direction * back_offset + [0, 0, height]
        #   focal_point = pos + direction * 0.5   (смотрим на стрелку)
        # -----------------------------------------------------
        back_offset = 0.3      # насколько позади стрелки
        height_offset = 0.4   # насколько выше стрелки

        camera_position = pos - direction * back_offset + np.array([0, 0, height_offset])
        camera_target = pos + direction * 0.5  # смотрим на тело стрелки

        plotter.camera.position = camera_position.tolist()
        plotter.camera.focal_point = camera_target.tolist()
        plotter.camera.up = (0, 0, 1)

        plotter.update()
        time.sleep(FRAME_DELAY)