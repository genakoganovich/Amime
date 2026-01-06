import numpy as np
import pyvista as pv
import time

from motion.trajectory import (
    interpolate_position_by_length,
    cumulative_lengths,
)

from motion.kinematics import (
    frenet_frame,
    curvature,
    radius_of_curvature,
)


# ============================================================
# Utility: convert direction vector → Euler
# ============================================================
def direction_to_euler(vec: np.ndarray):
    dx, dy, dz = vec
    yaw = np.degrees(np.arctan2(dy, dx))
    pitch = np.degrees(np.arctan2(dz, np.hypot(dx, dy)))
    roll = 0.0
    return pitch, yaw, roll


# ============================================================
# MAIN CLASS
# ============================================================
class KinematicVisualizer:

    def __init__(self, points: np.ndarray, steps=200, delay=0.03):

        # --------------------------
        # Input data
        # --------------------------
        self.points = points
        self.steps = steps
        self.delay = delay

        # --------------------------
        # Precompute kinematics
        # --------------------------
        self.cum_len = cumulative_lengths(points)
        self.total_len = self.cum_len[-1]

        self.T, self.N, self.B = frenet_frame(points)
        self.kappa = curvature(points)
        self.R = radius_of_curvature(points)

        # --------------------------
        # Create PyVista scene
        # --------------------------
        self._init_scene()

    # --------------------------------------------------------
    # Create plotter + actors
    # --------------------------------------------------------
    def _init_scene(self):

        self.plotter = pv.Plotter(window_size=(1400, 900))
        self.plotter.set_background("black")

        # draw path
        self.plotter.add_mesh(
            pv.lines_from_points(self.points),
            color="white",
            line_width=5,
        )

        # sphere (moving object)
        self.sphere_actor = self.plotter.add_mesh(
            pv.Sphere(radius=0.12),
            color="cyan"
        )

        # Frenet frame arrows
        self.arrow_T = self.plotter.add_mesh(pv.Arrow(scale=0.8), color="red")
        self.arrow_N = self.plotter.add_mesh(pv.Arrow(scale=0.6), color="green")
        self.arrow_B = self.plotter.add_mesh(pv.Arrow(scale=0.6), color="blue")

        # persistent text
        self.text_actor = self.plotter.add_text(
            "",
            position="upper_left",
            font_size=18,
            color="white"
        )

        # good camera
        self.plotter.camera.position = (3, -8, 4)
        self.plotter.camera.focal_point = (3, 0, 0)
        self.plotter.camera.up = (0, 0, 1)

        # enable interactive screen
        self.plotter.show(interactive_update=True)

    # --------------------------------------------------------
    # Update Frenet frame arrows for a given position
    # --------------------------------------------------------
    def _update_frenet_frame(self, pos, T_vec, N_vec, B_vec):

        for actor, vec, scale in [
            (self.arrow_T, T_vec, 0.8),
            (self.arrow_N, N_vec, 0.6),
            (self.arrow_B, B_vec, 0.6),
        ]:
            actor.SetPosition(pos)
            pitch, yaw, roll = direction_to_euler(vec)
            actor.SetOrientation(pitch, yaw, roll)
            actor.SetScale(scale)

    # --------------------------------------------------------
    # Update text HUD
    # --------------------------------------------------------
    def _update_text(self, s, seg_idx):

        msg = (
            f"s = {s:.3f}\n"
            f"segment = {seg_idx}\n"
            f"curvature κ = {self.kappa[seg_idx]:.3f}\n"
            f"radius R = {self.R[seg_idx]:.3f}"
        )

        # VTK-style SetText(index, text)
        self.text_actor.SetText(0, msg)

    # --------------------------------------------------------
    # Main animation loop
    # --------------------------------------------------------
    def run(self):
        while True:
            for i in range(self.steps):

                t = i / (self.steps - 1)
                s = t * self.total_len

                # position on curve
                pos = interpolate_position_by_length(self.points, s)

                # determine current segment
                seg = np.searchsorted(self.cum_len, s) - 1
                seg = np.clip(seg, 0, len(self.points) - 2)

                T_vec = self.T[seg]
                N_vec = self.N[seg]
                B_vec = self.B[seg]

                # update sphere
                self.sphere_actor.SetPosition(pos)

                # update Frenet frame
                self._update_frenet_frame(pos, T_vec, N_vec, B_vec)

                # update HUD
                self._update_text(s, seg)

                # render frame
                self.plotter.update()
                time.sleep(self.delay)