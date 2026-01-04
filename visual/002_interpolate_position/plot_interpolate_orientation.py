import pyvista as pv
import numpy as np
import time
from motion.trajectory import interpolate_orientation, cumulative_lengths, polyline_length

# -------------------------
# Траектория
# -------------------------
trajectory = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [4, 3, 0]
])

directions = interpolate_orientation(trajectory)
cum_lengths = cumulative_lengths(trajectory)
total_length = polyline_length(trajectory)

# -------------------------
# Настройка сцены
# -------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# вся траектория — желтая
mesh_traj = pv.lines_from_points(trajectory)
plotter.add_mesh(mesh_traj, color="yellow", line_width=3)

# шары
sphere_actor = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")
arrow_actor = plotter.add_mesh(pv.Arrow(direction=directions[0], scale=0.3), color="blue")

plotter.show(interactive_update=True)

# -------------------------
# Бесконечная анимация
# -------------------------
while True:
    for i, pos in enumerate(trajectory):
        # двигаем шар
        sphere_actor.SetPosition(pos)

        # двигаем стрелку
        arrow_actor.SetPosition(pos)
        arrow_actor.rotate_vector(directions[i], angle=0)  # сброс вращения
        arrow_actor.SetOrientation(np.degrees(np.arctan2(directions[i][1], directions[i][0])), 0, 0)

        # визуально выделяем пройденную часть красным
        if i > 0:
            passed_seg = trajectory[:i+1]
            mesh_passed = pv.lines_from_points(passed_seg)
            passed_actor = plotter.add_mesh(mesh_passed, color="red", line_width=5)

        plotter.update()
        time.sleep(0.5)

        # удаляем предыдущую красную линию, чтобы анимация повторялась заново
        if i > 0:
            plotter.remove_actor(passed_actor)

    # небольшая пауза в конце траектории
    time.sleep(1.0)
