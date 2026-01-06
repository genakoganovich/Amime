import pyvista as pv
import numpy as np

frame = 0


def on_timer(iren, event):
    global frame, cube_actor

    x = np.sin(frame * 0.05) * 2
    cube_actor.SetPosition(x, 0, 0)

    frame += 1

    plotter.render()


# ---------------------------------
# СЦЕНА
# ---------------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

cube = pv.Cube()
cube_actor = plotter.add_mesh(cube, color="cyan")

plotter.camera.position = (5, -5, 3)
plotter.camera.focal_point = (0, 0, 0)

# interactor
iren = plotter.iren

# 🔥 РАБОЧАЯ СВЯЗКА ДЛЯ ВАШЕЙ VTK
iren.add_observer("TimerEvent", on_timer)

# создать таймер 30 FPS
timer_id = iren.create_timer(33)

print("Timer created:", timer_id)

plotter.show()