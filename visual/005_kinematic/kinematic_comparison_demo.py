import numpy as np
import pyvista as pv
import time

from motion.trajectory import (
    interpolate_position,          # для неплавного движения
    interpolate_position_by_length, # для плавного движения
    interpolate_orientation,        # для неплавной ориентации
    cumulative_lengths,
    polyline_length,
)

from motion.kinematics import (
    frenet_frame,
)

from motion.visual_utils import (
    direction_to_euler,
    move_actor,
    apply_direction_to_actor,
)

# ================================================================
# CONFIGURATION
# ================================================================
FRAME_DELAY = 0.03
STEPS = 200

# Траектория с сегментами разной длины, чтобы было видно разницу в скорости
POINTS = np.array([
    [0, 0, 0],
    [1, 0.2, 0],      # короткий сегмент
    [3, 1.0, 0],      # длинный сегмент
    [3.5, 1.5, 0],    # короткий сегмент
    [4.0, 0.5, 0],    # короткий сегмент
    [6.0, -0.5, 0],   # длинный сегмент
    [7.0, -0.8, 0],
])

SPHERE_RADIUS = 0.1
ARROW_SCALE = 0.4
OFFSET_Y = 0.2 # Смещение по Y для объектов, чтобы они не накладывались

# ================================================================
# PRECOMPUTE KINEMATICS
# ================================================================
cum_len = cumulative_lengths(POINTS)
total_len = polyline_length(POINTS)

# Ориентация для "неплавного" объекта (по точкам)
non_smooth_directions = interpolate_orientation(POINTS)

# Фрейм Френе для "плавного" объекта (по точкам)
T_smooth, N_smooth, B_smooth = frenet_frame(POINTS)


# ================================================================
# PLOTTING SETUP
# ================================================================
plotter = pv.Plotter(window_size=(1400, 900))
plotter.set_background("black")

# Траектория
plotter.add_mesh(
    pv.lines_from_points(POINTS),
    color="white",
    line_width=5
)

# --- НЕПЛАВНЫЙ ОБЪЕКТ (красный) ---
sphere_ns = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="red"
)
arrow_ns = plotter.add_mesh(
    pv.Arrow(scale=ARROW_SCALE),
    color="red"
)
plotter.add_text("НЕПЛАВНОЕ ДВИЖЕНИЕ (индексы)", position=(0.02, 0.95), font_size=12, color="red")


# --- ПЛАВНЫЙ ОБЪЕКТ (голубой) ---
sphere_s = plotter.add_mesh(
    pv.Sphere(radius=SPHERE_RADIUS),
    color="cyan"
)
arrow_T_s = plotter.add_mesh(pv.Arrow(scale=ARROW_SCALE * 0.8), color="cyan") # Касательная для плавного
plotter.add_text("ПЛАВНОЕ ДВИЖЕНИЕ (длина дуги)", position=(0.02, 0.92), font_size=12, color="cyan")


# Камера (общая для обоих объектов)
plotter.camera.position = (3.5, -9, 4)
plotter.camera.focal_point = (3.5, 0, 0)
plotter.camera.up = (0, 0, 1)

plotter.show(interactive_update=True, auto_close=False)


# ================================================================
# MAIN ANIMATION LOOP
# ================================================================
while True:
    for i in range(STEPS):

        # Параметр прогресса (0.0 до 1.0)
        t_param = i / (STEPS - 1)

        # ----------------------------------------------------
        # НЕПЛАВНОЕ ДВИЖЕНИЕ (красный объект)
        # ----------------------------------------------------
        # Позиция по индексу (скорость меняется)
        t_index = t_param * (len(POINTS) - 1) # Параметр для interpolate_position
        pos_ns_on_path = interpolate_position(POINTS, t_index)
        pos_ns = pos_ns_on_path + np.array([0, -OFFSET_Y, 0]) # Смещение

        # Ориентация по сегментам (резкие повороты)
        seg_idx_ns = int(np.floor(t_index))
        seg_idx_ns = np.clip(seg_idx_ns, 0, len(non_smooth_directions) - 1)
        dir_ns = non_smooth_directions[seg_idx_ns]

        move_actor(sphere_ns, pos_ns)
        apply_direction_to_actor(arrow_ns, dir_ns, ARROW_SCALE)
        move_actor(arrow_ns, pos_ns)


        # ----------------------------------------------------
        # ПЛАВНОЕ ДВИЖЕНИЕ (голубой объект)
        # ----------------------------------------------------
        # Позиция по длине дуги (скорость постоянна)
        s = t_param * total_len # Расстояние по длине дуги
        pos_s_on_path = interpolate_position_by_length(POINTS, s)
        pos_s = pos_s_on_path + np.array([0, OFFSET_Y, 0]) # Смещение

        # Ориентация по Frenet frame (плавные повороты)
        seg_idx_s = np.searchsorted(cum_len, s) - 1
        seg_idx_s = np.clip(seg_idx_s, 0, len(POINTS) - 2)
        dir_s = T_smooth[seg_idx_s] # Касательная из Frenet frame

        move_actor(sphere_s, pos_s)
        apply_direction_to_actor(arrow_T_s, dir_s, ARROW_SCALE * 0.8) # Касательная
        move_actor(arrow_T_s, pos_s)


        # ----------------------------------------------------
        # RENDER
        # ----------------------------------------------------
        plotter.update()
        time.sleep(FRAME_DELAY)