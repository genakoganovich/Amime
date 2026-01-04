import pyvista as pv
import numpy as np
import time
from matplotlib import cm

# -------------------------
# Траектория
# -------------------------
t = np.linspace(0, 2*np.pi, 100)
trajectory = np.column_stack([np.cos(t), np.sin(t), t*0.1])

# Вычисляем накопленную длину
diffs = np.diff(trajectory, axis=0)
seg_lengths = np.linalg.norm(diffs, axis=1)
cum_lengths = np.concatenate([[0.0], np.cumsum(seg_lengths)])
total_length = cum_lengths[-1]

# -------------------------
# Настройка сцены
# -------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# Красный шар
sphere_actor = plotter.add_mesh(pv.Sphere(radius=0.08), color="red")

# Вся траектория — желтая базовая линия
plotter.add_lines(trajectory, color="yellow", width=2)

# -------------------------
# Интерактивный режим
# -------------------------
plotter.show(interactive_update=True)

# -------------------------
# Анимация с градиентом пройденной части
# -------------------------
passed_line_actor = None
for i, pos in enumerate(trajectory):
    sphere_actor.SetPosition(pos)

    # удаляем предыдущую красную линию
    if passed_line_actor is not None:
        plotter.remove_actor(passed_line_actor)

    if i > 0:
        passed_seg = trajectory[:i+1]

        # создаём линию сегментов
        mesh = pv.lines_from_points(passed_seg)

        # присваиваем каждому сегменту цвет по длине
        n_points = passed_seg.shape[0]
        colors = []
        for j in range(n_points):
            val = cum_lengths[j] / total_length
            rgba = cm.viridis(val)
            colors.append(rgba[:3])  # берем только RGB

        mesh["colors"] = np.array(colors)
        passed_line_actor = plotter.add_mesh(mesh, scalars="colors", rgb=True, line_width=5)

    plotter.update()
    time.sleep(0.03)
