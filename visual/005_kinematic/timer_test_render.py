import pyvista as pv
import numpy as np
import time

frame = 0
last_time = time.time()
fps = 30
dt = 1.0 / fps


def on_render(plotter):
    """
    PyVista вызывает callback как on_render(plotter),
    а не on_render(caller, event).
    """
    global frame, last_time, cube_actor

    now = time.time()

    # FPS throttling
    if now - last_time < dt:
        return

    last_time = now

    # движение куба
    x = np.sin(frame * 0.05) * 2
    cube_actor.SetPosition(x, 0, 0)
    frame += 1


# -----------------------------------------------------------
# сцена
# -----------------------------------------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

cube = pv.Cube()
cube_actor = plotter.add_mesh(cube, color="cyan")

plotter.camera.position = (5, -5, 3)
plotter.camera.focal_point = (0, 0, 0)

# РАБОЧЕЕ СОБЫТИЕ:
plotter.add_on_render_callback(on_render)

plotter.show()