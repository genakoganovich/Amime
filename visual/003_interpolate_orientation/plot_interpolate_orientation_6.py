import pyvista as pv
import numpy as np
import time
from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
    interpolate_position_by_length,
    interpolate_orientation,
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
total_length = polyline_length(TRAJECTORY)
cum_lengths = cumulative_lengths(TRAJECTORY)

# -------------------------
# Настройка сцены PyVista
# -------------------------
plotter = pv.Plotter()
plotter.set_background("black")

# Траектория
plotter.add_mesh(pv.lines_from_points(TRAJECTORY), color="yellow", line_width=3)

# Красный шар
sphere_actor = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS), color="red")

# Стрелка вдоль X
initial_dir = np.array([1, 0, 0])
arrow_mesh = pv.Arrow(direction=initial_dir, scale=ARROW_SCALE)
arrow_actor = plotter.add_mesh(arrow_mesh, color="blue")
arrow_actor.SetPosition(TRAJECTORY[0])
last_direction = directions[0].copy()

plotter.show(interactive_update=True)

# -------------------------
# Вспомогательная функция вращения 3D стрелки
# -------------------------
def rotate_arrow(actor, from_dir, to_dir):
    """Вращает actor из from_dir в to_dir только если направление изменилось"""
    from_dir = from_dir / np.linalg.norm(from_dir)
    to_dir = to_dir / np.linalg.norm(to_dir)
    axis = np.cross(from_dir, to_dir)
    if np.linalg.norm(axis) < 1e-6:
        return  # направление не изменилось или противоположно
    angle = np.degrees(np.arccos(np.clip(np.dot(from_dir, to_dir), -1.0, 1.0)))
    actor.RotateWXYZ(angle, *axis)

# -------------------------
# Анимация
# -------------------------
while True:
    for i in range(STEPS):
        # Текущая длина по траектории
        s = i * total_length / (STEPS - 1)
        pos = interpolate_position_by_length(TRAJECTORY, s)
        sphere_actor.SetPosition(pos)

        # Находим сегмент и направление
        seg_idx = np.searchsorted(cum_lengths, s, side="right") - 1
        seg_idx = np.clip(seg_idx, 0, len(directions) - 1)
        direction = directions[seg_idx]

        # Вращаем стрелку только если направление изменилось
        if not np.allclose(direction, last_direction):
            rotate_arrow(arrow_actor, last_direction, direction)
            last_direction = direction.copy()

        # Перемещаем стрелку
        arrow_actor.SetPosition(pos)

        # Обновляем сцену
        plotter.update()
        time.sleep(FRAME_DELAY)

    # Пауза в конце траектории
    time.sleep(PAUSE_END)
