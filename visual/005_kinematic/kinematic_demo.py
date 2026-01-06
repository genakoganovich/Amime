import numpy as np
import pyvista as pv
import time

from motion.trajectory import (
    interpolate_position_by_length,
    cumulative_lengths,
    interpolate_orientation,
)

from motion.kinematics import (
    frenet_frame,
    curvature,
    radius_of_curvature,
)

# ================================================================
# CONFIG
# ================================================================
FRAME_DELAY = 0.03
STEPS = 200

POINTS = np.array([
    [0, 0, 0],
    [1, 0.2, 0],
    [2, 1.0, 0],
    [3, 1.2, 0],
    [4, 0.5, 0],
    [5, -0.5, 0],
    [6, -0.8, 0],
])

# ================================================================
# PRECOMPUTE KINEMATICS
# ================================================================
cum_len = cumulative_lengths(POINTS)
total_len = cum_len[-1]

T, N, B = frenet_frame(POINTS)
kappa = curvature(POINTS)
R = radius_of_curvature(POINTS)

# ================================================================
# PLOTTING SETUP
# ================================================================
plotter = pv.Plotter(window_size=(1400, 900))
plotter.set_background("black")

# Path
plotter.add_mesh(
    pv.lines_from_points(POINTS),
    color="white",
    line_width=5
)

# Moving sphere — larger and bright
sphere_actor = plotter.add_mesh(
    pv.Sphere(radius=0.12),
    color="cyan"
)

# Frenet frame arrows (tangent, normal, binormal)
arrow_T = plotter.add_mesh(pv.Arrow(scale=0.8), color="red")
arrow_N = plotter.add_mesh(pv.Arrow(scale=0.6), color="green")
arrow_B = plotter.add_mesh(pv.Arrow(scale=0.6), color="blue")

# Persistent text actor
text_actor = plotter.add_text(
    "",
    position="upper_left",
    font_size=18,
    color="white"
)

# Good camera view
plotter.camera.position = (3, -8, 4)
plotter.camera.focal_point = (3, 0, 0)
plotter.camera.up = (0, 0, 1)

plotter.show(interactive_update=True)


# ================================================================
# Convert direction vector → Euler angles
# ================================================================
def direction_to_euler(vec):
    dx, dy, dz = vec
    yaw = np.degrees(np.arctan2(dy, dx))                # rotate around Z
    pitch = np.degrees(np.arctan2(dz, np.hypot(dx, dy)))  # rotate around Y
    return pitch, yaw, 0.0


# ================================================================
# MAIN LOOP
# ================================================================
while True:
    for i in range(STEPS):

        # Progress along path
        t = i / (STEPS - 1)
        s = t * total_len

        pos = interpolate_position_by_length(POINTS, s)

        seg = np.searchsorted(cum_len, s) - 1
        seg = np.clip(seg, 0, len(POINTS) - 2)

        T_vec = T[seg]
        N_vec = N[seg]
        B_vec = B[seg]

        k_val = kappa[seg]
        R_val = R[seg]

        # ------------------------------
        # Update sphere
        # ------------------------------
        sphere_actor.SetPosition(pos)

        # ------------------------------
        # Update all Frenet arrows
        # ------------------------------
        for actor, vec, scale in [
            (arrow_T, T_vec, 0.8),
            (arrow_N, N_vec, 0.6),
            (arrow_B, B_vec, 0.6),
        ]:
            actor.SetPosition(pos)
            pitch, yaw, roll = direction_to_euler(vec)
            actor.SetOrientation(pitch, yaw, roll)
            actor.SetScale(scale)

        # ------------------------------
        # Update text (correct VTK version)
        # ------------------------------
        msg = (
            f"s = {s:.3f}\n"
            f"segment = {seg}\n"
            f"curvature κ = {k_val:.3f}\n"
            f"radius R = {R_val:.3f}"
        )
        text_actor.SetText(0, msg)   # <— FIXED

        # ------------------------------
        # Render frame
        # ------------------------------
        plotter.update()
        time.sleep(FRAME_DELAY)