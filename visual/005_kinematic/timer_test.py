import pyvista as pv
import numpy as np


# глобальный счётчик
frame = 0


def on_timer(caller, event):
    global frame, cube_actor

    # движение куба по синусу
    x = np.sin(frame * 0.05) * 2
    y = 0
    z = 0

    cube_actor.SetPosition(x, y, z)
    frame += 1

    plotter.render()


# -------------------------------------------------------------
# главный код
# -------------------------------------------------------------
plotter = pv.Plotter(window_size=(800, 600))
plotter.set_background("black")

# создаём куб
cube = pv.Cube()
cube_actor = plotter.add_mesh(cube, color="cyan")

# камера
plotter.camera.position = (6, -6, 4)
plotter.camera.focal_point = (0, 0, 0)

# interactor (RenderWindowInteractor)
iren = plotter.iren

# ------------------------------------------
# Подключаем callback
# ------------------------------------------
try:
    iren.add_observer("TimerEvent", on_timer)
except Exception as e:
    print("add_observer НЕ работает:", e)
    raise

# ------------------------------------------
# Создаём repeating timer
# ------------------------------------------
interval_ms = 33  # ~30 FPS

# Пытаемся найти метод таймера
if hasattr(iren, "create_repeating_timer"):
    timer_id = iren.create_repeating_timer(interval_ms)
elif hasattr(iren, "CreateRepeatingTimer"):
    timer_id = iren.CreateRepeatingTimer(interval_ms)
else:
    raise RuntimeError("Не найден метод таймера (create_repeating_timer / CreateRepeatingTimer)")

print(f"Timer ID: {timer_id}")

# запускаем окно
plotter.show()