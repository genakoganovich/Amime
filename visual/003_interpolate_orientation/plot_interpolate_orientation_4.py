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
# Траектория и направления
# -------------------------
trajectory = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

directions = interpolate_orientation(trajectory)
total_length = polyline_length(trajectory)
cum_lengths = cumulative_lengths(trajectory)

# -------------------------
# Настройка сцены PyVista
# -------------------------
plotter = pv.Plotter()
plotter.set_background("black")

# Траектория
plotter.add_mesh(pv.lines_from_points(trajectory), color="yellow", line_width=3)

# Красный шар
sphere = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")

# Инициализация стрелки вдоль X (будет повернута при необходимости)
arrow_actor = pv.Arrow(direction=(1, 0, 0), scale=0.4)
arrow_actor = plotter.add_mesh(arrow_actor, color="blue")
arrow_actor.SetPosition(trajectory[0])
last_direction = directions[0].copy()  # текущее направление

# Включаем интерактивное обновление
plotter.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
steps = 150

while True:
    for i in range(steps):
        # Текущая пройденная длина по траектории
        s = i * total_length / (steps - 1)
        pos = interpolate_position_by_length(trajectory, s)

        # Находим сегмент и направление
        seg_idx = np.searchsorted(cum_lengths, s, side="right") - 1
        seg_idx = np.clip(seg_idx, 0, len(directions) - 1)
        direction = directions[seg_idx]

        # Обновляем позицию шара
        sphere.SetPosition(pos)

        # --- пересоздаём стрелку только если направление изменилось ---
        if not np.allclose(direction, last_direction):
            plotter.remove_actor(arrow_actor)
            arrow_actor = plotter.add_mesh(
                pv.Arrow(direction=direction, scale=0.4),
                color="blue",
            )
            last_direction = direction.copy()

        # Обновляем позицию стрелки
        arrow_actor.SetPosition(pos)

        # Обновляем сцену
        plotter.update()
        time.sleep(0.03)

    # Пауза в конце траектории
    time.sleep(1.0)
