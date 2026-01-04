import pyvista as pv
import numpy as np
import time

# -------------------------
# Траектория
# -------------------------
t = np.linspace(0, 2*np.pi, 100)
trajectory = np.column_stack([np.cos(t), np.sin(t), t*0.1])

# -------------------------
# Настройка сцены
# -------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# красный шар
sphere_actor = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")

# вся траектория — желтая
plotter.add_lines(trajectory, color="yellow", width=3)

# -------------------------
# Запуск интерактивного режима
# -------------------------
plotter.show(interactive_update=True)

# -------------------------
# Бесконечная анимация с перезапуском
# -------------------------
while True:
    passed_line_actors = []  # будем хранить все сегменты красной линии

    for i, pos in enumerate(trajectory):
        sphere_actor.SetPosition(pos)

        # удаляем предыдущие сегменты красной линии
        for actor in passed_line_actors:
            plotter.remove_actor(actor)
        passed_line_actors = []

        # создаём пройденную часть как линии через pv.lines_from_points
        if i > 0:
            passed_seg = trajectory[:i+1]
            mesh = pv.lines_from_points(passed_seg)
            actor = plotter.add_mesh(mesh, color="red", line_width=5)
            passed_line_actors.append(actor)

        plotter.update()
        time.sleep(0.03)

    # пауза в конце траектории
    time.sleep(1.0)
