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

# ======================================================
# Конфигурация
# ======================================================
TRAJECTORY = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

ARROW_SCALE = 0.35
SPHERE_RADIUS = 0.1
STEPS = 150
FRAME_DELAY = 0.03
PAUSE_END = 1.0

# ======================================================
# Подготовка данных
# ======================================================
directions = interpolate_orientation(TRAJECTORY)
cum_lengths = cumulative_lengths(TRAJECTORY)
total_length = polyline_length(TRAJECTORY)

# ======================================================
# Создаём сцену PyVista с двумя окнами (subplot 1x2)
# ======================================================
plotter = pv.Plotter(shape=(1, 2))
plotter.set_background("black")

# ======================================================
# Левое окно — interpolate_orientation (дискретная ориентация)
# ======================================================
plotter.subplot(0, 0)
plotter.add_text("interpolate_orientation", font_size=12)

plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3,
)

sphere_left = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="red",
)

arrow_left = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="cyan",
)
arrow_left.SetPosition(TRAJECTORY[0])
last_direction_left = np.array([1.0, 0.0, 0.0])


def rotate_arrow(actor, from_dir, to_dir):
    """Плавный поворот стрелки из одного 3D направления в другое."""
    from_dir = from_dir / np.linalg.norm(from_dir)
    to_dir = to_dir / np.linalg.norm(to_dir)
    axis = np.cross(from_dir, to_dir)

    if np.linalg.norm(axis) < 1e-6:
        return  # направления коллинеарны

    angle = np.degrees(
        np.arccos(
            np.clip(np.dot(from_dir, to_dir), -1.0, 1.0)
        )
    )
    actor.RotateWXYZ(angle, *axis)


# ======================================================
# Правое окно — interpolate_orientation_by_length (непрерывная ориентация)
# ======================================================
plotter.subplot(0, 1)
plotter.add_text("interpolate_orientation_by_length", font_size=12)

plotter.add_mesh(
    pv.lines_from_points(TRAJECTORY),
    color="yellow",
    line_width=3,
)

sphere_right = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="red",
)

arrow_right = plotter.add_mesh(
    pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
    color="cyan",
)
arrow_right.SetPosition(TRAJECTORY[0])
last_direction_right = np.array([1.0, 0.0, 0.0])


# ======================================================
# Запуск интерактивной сцены
# ======================================================
plotter.show(interactive_update=True)

# ======================================================
# Основная анимация
# ======================================================
while True:
    for i in range(STEPS):
        s = i * total_length / (STEPS - 1)

        # ---------------- ЛЕВАЯ визуализация ----------------
        pos = interpolate_position_by_length(TRAJECTORY, s)
        sphere_left.SetPosition(pos)

        seg_idx = np.searchsorted(cum_lengths, s, side="right") - 1
        seg_idx = np.clip(seg_idx, 0, len(directions) - 1)
        direction_left = directions[seg_idx]

        if not np.allclose(direction_left, last_direction_left):
            rotate_arrow(arrow_left, last_direction_left, direction_left)
            last_direction_left = direction_left.copy()

        arrow_left.SetPosition(pos)

        # ---------------- ПРАВАЯ визуализация ----------------
        pos_r = pos
        sphere_right.SetPosition(pos_r)

        direction_right = interpolate_orientation_by_length(
            cum_lengths,
            directions[:-1],
            s,
        )

        if not np.allclose(direction_right, last_direction_right):
            yaw = np.degrees(np.arctan2(direction_right[1], direction_right[0]))
            arrow_right.SetOrientation(0.0, 0.0, yaw)
            last_direction_right = direction_right.copy()

        arrow_right.SetPosition(pos_r)

        plotter.update()
        time.sleep(FRAME_DELAY)

    time.sleep(PAUSE_END)