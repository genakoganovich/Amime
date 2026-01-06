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
    move_actor,
    direction_to_euler,
)

print(">>> KinematicVisualizerOptimized LOADED <<<")
class KinematicVisualizerOptimized:
    """
    Оптимизированный визуализатор на основе цикла.
    Теперь с поддержкой расширений (features),
    и КОРРЕКТНЫМ порядком запуска (show() — только в run()).
    """

    def __init__(self, points, steps=200, fps=30, autorun=True):
        self.points = np.asarray(points)
        self.steps = steps
        self.fps = fps
        self.dt = 1.0 / fps

        # --- kinematics ---
        self.cum = cumulative_lengths(self.points)
        self.total_len = self.cum[-1]

        self.T, self.N, self.B = frenet_frame(self.points)
        self.kappa = curvature(self.points)
        self.R = radius_of_curvature(self.points)

        # --- caches ---
        self.prev_pos = None
        self.prev_T = None
        self.prev_N = None
        self.prev_B = None
        self.prev_seg = -1

        # --- features ---
        self.features = []

        self.step = 0

        self._init_scene()

        if autorun:
            self.run()

    # ==========================================================
    # Feature system
    # ==========================================================
    def add_feature(self, feature):
        feature.initialize(self.plotter)
        self.features.append(feature)
        print("[DEBUG] Feature added:", feature)
        print("[DEBUG] Total features:", len(self.features))

    # ==========================================================
    # Scene
    # ==========================================================
    def _init_scene(self):
        self.plotter = pv.Plotter(window_size=(1400, 900))
        self.plotter.set_background("black")

        # trajectory
        self.plotter.add_mesh(
            pv.lines_from_points(self.points),
            color="white",
            line_width=5
        )

        # sphere
        self.sphere = self.plotter.add_mesh(
            pv.Sphere(radius=0.12),
            color="cyan"
        )

        # Frenet arrows
        self.arrow_T = self.plotter.add_mesh(pv.Arrow(), color="red")
        self.arrow_T.SetScale(0.8)

        self.arrow_N = self.plotter.add_mesh(pv.Arrow(), color="green")
        self.arrow_N.SetScale(0.6)

        self.arrow_B = self.plotter.add_mesh(pv.Arrow(), color="blue")
        self.arrow_B.SetScale(0.6)

        # text
        self.text_actor = self.plotter.add_text(
            "",
            position="upper_left",
            font_size=16,
            color="white"
        )

        # camera
        self.plotter.camera.position = (3, -8, 4)
        self.plotter.camera.focal_point = (3, 0, 0)
        self.plotter.camera.up = (0, 0, 1)

        # ❗ ВАЖНО: show() не вызываем здесь!
        # show() будет вызываться в run()

    # ==========================================================
    # Main animation loop
    # ==========================================================
    def run(self):
        """Main animation loop — callable after adding features."""
        # теперь можно показать окно
        self.plotter.show(interactive_update=True, auto_close=False)


        while True:

            frame_start = time.perf_counter()

            step = self.step
            self.step = (self.step + 1) % self.steps

            t = step / (self.steps - 1)
            s = t * self.total_len

            pos = interpolate_position_by_length(self.points, s)

            seg = np.searchsorted(self.cum, s) - 1
            seg = np.clip(seg, 0, len(self.points) - 2)

            T_vec = self.T[seg]
            N_vec = self.N[seg]
            B_vec = self.B[seg]

            print("kappa:", self.kappa)
            print("R:", self.R)
            print("s =", s)
            print("cum_len:", self.cum)
            print("step:", step, "s:", s, "seg:", seg)
            # -----------------------------------------------------
            # SPHERE (dirty update)
            # -----------------------------------------------------
            if self.prev_pos is None or not np.allclose(pos, self.prev_pos):
                move_actor(self.sphere, pos)
                move_actor(self.arrow_T, pos)
                move_actor(self.arrow_N, pos)
                move_actor(self.arrow_B, pos)
                self.prev_pos = pos

            # -----------------------------------------------------
            # ARROWS (dirty)
            # -----------------------------------------------------
            self._update_arrow(self.arrow_T, T_vec, "prev_T")
            self._update_arrow(self.arrow_N, N_vec, "prev_N")
            self._update_arrow(self.arrow_B, B_vec, "prev_B")

            # -----------------------------------------------------
            # HUD text
            # -----------------------------------------------------
            if seg != self.prev_seg:
                msg = (
                    f"s = {s:.3f}\n"
                    f"segment = {seg}\n"
                    f"curvature κ = {self.kappa[seg]:.3f}\n"
                    f"radius R = {self.R[seg]:.3f}"
                )
                self.text_actor.SetText(0, msg)
                self.prev_seg = seg

            # -----------------------------------------------------
            # FEATURE UPDATE
            # -----------------------------------------------------
            if len(self.features) > 0:
                print(f"[DEBUG] Running features: {len(self.features)}", flush=True)

            state = {
                "pos": pos,
                "T": T_vec,
                "N": N_vec,
                "B": B_vec,
                "curvature": self.kappa[seg],
                "radius": self.R[seg],
                "seg": seg,
                "s": s,
            }

            for f in self.features:
                print("[DEBUG] Calling feature.update", f, flush=True)
                f.update(state)

            # -----------------------------------------------------
            # Render
            # -----------------------------------------------------
            self.plotter.update()

            # FPS
            elapsed = time.perf_counter() - frame_start
            if elapsed < self.dt:
                time.sleep(self.dt - elapsed)

    # ==========================================================
    def _update_arrow(self, actor, vec, cache_name):
        prev = getattr(self, cache_name)
        if prev is not None and np.allclose(prev, vec):
            return

        pitch, yaw, roll = direction_to_euler(vec)
        actor.SetOrientation(pitch, yaw, roll)
        setattr(self, cache_name, vec)