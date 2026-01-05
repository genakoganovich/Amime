import pyvista as pv
import numpy as np
import time
from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
    interpolate_position_by_length,
    interpolate_orientation,
)

trajectory = np.array([
    [0,0,0],
    [0.5,0,0],
    [2,0,0],
    [2,1,0],
    [3,1,0],
    [3,3,0],
])

directions = interpolate_orientation(trajectory)
total_length = polyline_length(trajectory)


plotter = pv.Plotter()
plotter.set_background("black")

plotter.add_mesh(pv.lines_from_points(trajectory), color="yellow", line_width=3)

sphere = plotter.add_mesh(pv.Sphere(radius=0.1), color="red")
arrow_actor = None

plotter.show(interactive_update=True)

steps = 150

while True:
    for i in range(steps):
        s = i * total_length / (steps - 1)
        pos = interpolate_position_by_length(trajectory, s)

        idx = np.argmin(np.linalg.norm(trajectory - pos, axis=1))
        direction = directions[idx]

        sphere.SetPosition(pos)

        # удаляем старую стрелку
        if arrow_actor is not None:
            plotter.remove_actor(arrow_actor)

        # создаём новую стрелку с нужным направлением
        arrow_actor = plotter.add_mesh(
            pv.Arrow(direction=direction, scale=0.4),
            color="blue",
        )
        arrow_actor.SetPosition(pos)

        plotter.update()
        time.sleep(0.03)

    time.sleep(1.0)

