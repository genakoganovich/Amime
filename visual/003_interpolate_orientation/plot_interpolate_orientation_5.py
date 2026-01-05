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
# Вспомогательные функции
# -------------------------
def create_plotter():
    plotter = pv.Plotter()
    plotter.set_background("black")
    plotter.add_mesh(pv.lines_from_points(TRAJECTORY), color="yellow", line_width=3)
    return plotter


def create_sphere(plotter):
    return plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS), color="red")


def create_arrow(plotter, direction, position):
    actor = pv.Arrow(direction=direction, scale=ARROW_SCALE)
    actor = plotter.add_mesh(actor, color="blue")
    actor.SetPosition(position)
    return actor


def get_direction_at_length(s, cum_lengths, directions):
    idx = np.searchsorted(cum_lengths, s, side="right") - 1
    idx = np.clip(idx, 0, len(directions) - 1)
    return directions[idx]


# -------------------------
# Подготовка данных
# -------------------------
directions = interpolate_orientation(TRAJECTORY)
total_length = polyline_length(TRAJECTORY)
cum_lengths = cumulative_lengths(TRAJECTORY)

# -------------------------
# Настройка сцены PyVista
# -------------------------
plotter = create_plotter()
sphere_actor = create_sphere(plotter)
arrow_actor = create_arrow(plotter, directions[0], TRAJECTORY[0])
last_direction = directions[0].copy()

plotter.show(interactive_update=True)

# -------------------------
# Анимация
# -------------------------
while True:
    for i in range(STEPS):
        # Текущая длина по траектории
        s = i * total_length / (STEPS - 1)
        pos = interpolate_position_by_length(TRAJECTORY, s)
        direction = get_direction_at_length(s, cum_lengths, directions)

        # Обновляем позицию шара
        sphere_actor.SetPosition(pos)

        # Пересоздаём стрелку только если направление изменилось
        if not np.allclose(direction, last_direction):
            plotter.remove_actor(arrow_actor)
            arrow_actor = create_arrow(plotter, direction, pos)
            last_direction = direction.copy()
        else:
            # Иначе просто перемещаем стрелку
            arrow_actor.SetPosition(pos)

        plotter.update()
        time.sleep(FRAME_DELAY)

    # Пауза в конце траектории
    time.sleep(PAUSE_END)
