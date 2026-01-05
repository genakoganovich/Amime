import pyvista as pv
import numpy as np
import time
from scipy.spatial.transform import Rotation as R

from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
)


# -----------------------------------------------------
# Траектория
# -----------------------------------------------------
TRAJECTORY = np.array([
    [0, 0, 0],
    [0.5, 0, 0],
    [2, 0, 0],
    [2, 1, 0],
    [3, 1, 0],
    [3, 3, 0],
])

SPHERE_RADIUS = 0.12
ARROW_SCALE = 0.3
STEPS = 150
FRAME_DELAY = 0.03

# -----------------------------------------------------
# Данные траектории
# -----------------------------------------------------
cum_len = cumulative_lengths(TRAJECTORY)
total_len = polyline_length(TRAJECTORY)
directions = interpolate_orientation(TRAJECTORY)


# -----------------------------------------------------
#  SLERP helper
# -----------------------------------------------------
from scipy.spatial.transform import Slerp

def slerp_rot(r0, r1, t):
    key_times = [0, 1]
    key_rots = R.from_quat([r0.as_quat(), r1.as_quat()])
    slerp = Slerp(key_times, key_rots)
    return slerp([t])[0]


# -----------------------------------------------------
# PyVista Scene with 2 subplots
# -----------------------------------------------------
plotter = pv.Plotter(shape=(1, 2))
plotter.set_background("black")


# =====================================================
# LEFT SUBPLOT — обычная follow camera
# =====================================================
plotter.subplot(0, 0)
plotter.add_text("FOLLOW CAMERA (обычная)", font_size=14)

plotter.add_mesh(pv.lines_from_points(TRAJECTORY), color="yellow", line_width=3)

sphere_actor = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS), color="cyan")
arrow_actor = plotter.add_mesh(pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
                               color="cyan")


# =====================================================
# RIGHT SUBPLOT — кинематографичная camera
# =====================================================
plotter.subplot(0, 1)
plotter.add_text("CINEMATIC CAMERA (smooth + slerp)", font_size=14)

plotter.add_mesh(pv.lines_from_points(TRAJECTORY), color="yellow", line_width=3)

sphere_actor2 = plotter.add_mesh(pv.Sphere(radius=SPHERE_RADIUS), color="cyan")
arrow_actor2 = plotter.add_mesh(pv.Arrow(direction=(1, 0, 0), scale=ARROW_SCALE),
                                color="cyan")

# cinematic state
cin_cam_pos = np.array([0.0, -20.0, 4])
cin_cam_rot = R.from_euler("xyz", [0, 0, 0], degrees=True)


plotter.show(interactive_update=True)


# -----------------------------------------------------
# АНИМАЦИЯ
# -----------------------------------------------------
while True:
    for i in range(STEPS):
        t = i / (STEPS - 1)
        s = t * total_len

        # основное положение стрелки
        pos = interpolate_position_by_length(TRAJECTORY, s)
        direction = interpolate_orientation_by_length(cum_len, directions[:-1], s)
        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        # -------------------------------------------------
        # LEFT VIEW (обычная follow camera)
        # -------------------------------------------------
        plotter.subplot(0, 0)

        sphere_actor.SetPosition(pos)
        arrow_actor.SetPosition(pos)
        arrow_actor.SetOrientation(0, 0, yaw)

        # камера просто прицеплена позади стрелки
        back = pos - direction * 0.4 + np.array([0, -1.5, 0.4])
        forward = pos + direction * 0.5

        plotter.camera.position = back.tolist()
        plotter.camera.focal_point = forward.tolist()
        plotter.camera.up = (0, 0, 1)

        # -------------------------------------------------
        # RIGHT VIEW — CINEMATIC CAMERA
        # -------------------------------------------------
        plotter.subplot(0, 1)

        sphere_actor2.SetPosition(pos)
        arrow_actor2.SetPosition(pos)
        arrow_actor2.SetOrientation(0, 0, yaw)

        # desired camera position behind arrow
        desired_pos = pos - direction * 0.8 + np.array([0, 0, 0.35])

        # smooth follow (lerp)
        cin_cam_pos = 0.92 * cin_cam_pos + 0.08 * desired_pos

        # desired rotation
        fwd = direction / np.linalg.norm(direction)
        up = np.array([0, 0, 1.0])

        # build rotation matrix: columns [right, up', forward]
        right = np.cross(up, fwd)
        if np.linalg.norm(right) < 1e-6:
            right = np.array([1, 0, 0])
        right /= np.linalg.norm(right)
        up2 = np.cross(fwd, right)

        desired_rot = R.from_matrix(np.vstack([right, up2, fwd]).T)

        # SLERP rotation smoothing
        cin_cam_rot = slerp_rot(cin_cam_rot, desired_rot, 0.07)

        # apply
        rot_matrix = cin_cam_rot.as_matrix()
        focal_point = cin_cam_pos + rot_matrix[:, 2] * 2.0  # look forward

        plotter.camera.position = cin_cam_pos.tolist()
        plotter.camera.focal_point = focal_point.tolist()
        plotter.camera.up = rot_matrix[:, 1].tolist()

        # update
        plotter.update()
        time.sleep(FRAME_DELAY)