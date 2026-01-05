import pyvista as pv
import numpy as np
import time
from scipy.spatial.transform import Rotation as R

from motion.quaternions import (
    quat_from_direction,
    quat_slerp,
)

from motion.camera import camera_frame_target
from motion.trajectory import (
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
    cumulative_lengths,
    polyline_length,
)

# ---------------------------------------------------------
# TRAJECTORY
# ---------------------------------------------------------
TRAJECTORY = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 2.5, 0],
])

SPHERE_RADIUS = 0.08
ARROW_SCALE = 0.25
FRAME_DELAY = 0.03
STEPS = 180

cum_len = cumulative_lengths(TRAJECTORY)
total_len = polyline_length(TRAJECTORY)
directions = interpolate_orientation(TRAJECTORY)

# ---------------------------------------------------------
# PLOTTER (ONE CAMERA ONLY)
# ---------------------------------------------------------
plotter = pv.Plotter()
plotter.set_background("black")

# линия траектории
plotter.add_mesh(pv.lines_from_points(TRAJECTORY),
                 color="yellow", line_width=3)

# Объект A — обычная yaw-ориентация
sphere_A = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS),
                            color="red")
arrow_A = plotter.add_mesh(pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
                           color="red")

# Объект B — кватернионы (SLERP)
sphere_B = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS),
                            color="cyan")
arrow_B = plotter.add_mesh(pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
                           color="cyan")

# начальная ориентация B
cam_rot_B = quat_from_direction(np.array([1, 0, 0]))

plotter.show(interactive_update=True)

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
while True:
    for step in range(STEPS):

        t = step / (STEPS - 1)
        s = t * total_len

        pos = interpolate_position_by_length(TRAJECTORY, s)
        direction = interpolate_orientation_by_length(cum_len, directions[:-1], s)

        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        # -------------------------------
        # OBJECT A — YAW ONLY (дерганый)
        # -------------------------------
        pos_A = pos + np.array([0, -0.1, 0])     # сдвигаем чуть в сторону
        sphere_A.SetPosition(pos_A)
        arrow_A.SetPosition(pos_A)
        arrow_A.SetOrientation(0, 0, yaw)

        # -------------------------------
        # OBJECT B — QUATERNION SLERP
        # -------------------------------
        pos_B = pos + np.array([0, 0.1, 0])      # сдвигаем на другую сторону
        sphere_B.SetPosition(pos_B)
        arrow_B.SetPosition(pos_B)

        # SLERP smooth orientation
        desired_rot = quat_from_direction(direction)
        cam_rot_B = quat_slerp(cam_rot_B, desired_rot, 0.10)

        # применяем матрицу как ориентацию
        rot_matrix = cam_rot_B.as_matrix()
        # forward = rot_matrix[:, 2] — Z ось
        # yaw вычисляем из forward
        yaw_slerp = np.degrees(np.arctan2(rot_matrix[1,2], rot_matrix[0,2]))
        arrow_B.SetOrientation(0, 0, yaw_slerp)

        # -------------------------------
        # SINGLE camera — framing BOTH
        # -------------------------------
        # SINGLE camera — framing BOTH
        mid = (pos_A + pos_B) / 2

        # --- RESET CAMERA EACH FRAME (fix black screen / one loop only) ---
        plotter.camera.position = np.array([4, -4, 3])
        plotter.camera.focal_point = np.array([1.5, 1.0, 0])
        plotter.camera.up = (0, 0, 1)

        # --- NOW framing works properly ---
        camera_frame_target(
            plotter,
            mid,
            distance=1.8,
            height=0.6,
            padding=1.25
        )

        plotter.update()
        time.sleep(FRAME_DELAY)