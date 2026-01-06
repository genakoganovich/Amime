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

from motion.visual_utils import (
    direction_to_euler,
    apply_direction_to_actor,
    move_actor,
)


class KinematicVisualizer:
    """
    Визуализатор кинематики движения по траектории с Frenet–Serret рамкой.
    """

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self, points: np.ndarray, steps=200, delay=0.03):

        # Input trajectory
        self.points = points
        self.steps = steps
        self.delay = delay

        # Precompute kinematics
        self.cum_len = cumulative_lengths(points)
        self.total_len = self.cum_len[-1]

        self.T, self.N, self.B = frenet_frame(points)
        self.kappa = curvature(points)
        self.R = radius_of_curvature(points)

        # Initialize scene & actors
        self._init_scene()

    # ----------------------------------------------------------------------
    # Create scene and graphical actors
    # ----------------------------------------------------------------------
    def _init_scene(self):
        self.plotter = pv.Plotter(window_size=(1400, 900))
        self.plotter.set_background("black")

        # Draw trajectory
        self.plotter.add_mesh(
            pv.lines_from_points(self.points),
            color="white",
            line_width=5,
        )

        # Moving sphere
        self.sphere_actor = self.plotter.add_mesh(
            pv.Sphere(radius=0.12),
            color="cyan",
        )

        # Frenet frame arrows
        self.arrow_T = self.plotter.add_mesh(pv.Arrow(scale=0.8), color="red")
        self.arrow_N = self.plotter.add_mesh(pv.Arrow(scale=0.6), color="green")
        self.arrow_B = self.plotter.add_mesh(pv.Arrow(scale=0.6), color="blue")

        # Text HUD (static actor)
        self.text_actor = self.plotter.add_text(
            "",
            position="upper_left",
            font_size=18,
            color="white",
        )

        # Good camera placement
        self.plotter.camera.position = (3, -8, 4)
        self.plotter.camera.focal_point = (3, 0, 0)
        self.plotter.camera.up = (0, 0, 1)

        self.plotter.show(interactive_update=True)

    # ----------------------------------------------------------------------
    # Update Frenet–Serret arrows at position
    # ----------------------------------------------------------------------
    def _update_frenet_frame(self, pos, T_vec, N_vec, B_vec):
        apply_direction_to_actor(self.arrow_T, T_vec, scale=0.8)
        move_actor(self.arrow_T, pos)

        apply_direction_to_actor(self.arrow_N, N_vec, scale=0.6)
        move_actor(self.arrow_N, pos)

        apply_direction_to_actor(self.arrow_B, B_vec, scale=0.6)
        move_actor(self.arrow_B, pos)

    # ----------------------------------------------------------------------
    # Update on-screen text panel
    # ----------------------------------------------------------------------
    def _update_text(self, s, seg):
        msg = (
            f"s = {s:.3f}\n"
            f"segment = {seg}\n"
            f"curvature κ = {self.kappa[seg]:.3f}\n"
            f"radius R = {self.R[seg]:.3f}"
        )
        self.text_actor.SetText(0, msg)

    # ----------------------------------------------------------------------
    # Main animation loop
    # ----------------------------------------------------------------------
    def run(self):
        while True:
            for step in range(self.steps):

                t = step / (self.steps - 1)
                s = t * self.total_len

                # position on path
                pos = interpolate_position_by_length(self.points, s)

                # determine current segment
                seg = np.searchsorted(self.cum_len, s) - 1
                seg = np.clip(seg, 0, len(self.points) - 2)

                # Frenet frame vectors
                T_vec = self.T[seg]
                N_vec = self.N[seg]
                B_vec = self.B[seg]

                # update sphere position
                move_actor(self.sphere_actor, pos)

                # update arrows
                self._update_frenet_frame(pos, T_vec, N_vec, B_vec)

                # update HUD
                self._update_text(s, seg)

                # render frame
                self.plotter.update()
                time.sleep(self.delay)