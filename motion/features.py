import numpy as np
import pyvista as pv


class KinematicFeature:
    def initialize(self, plotter):
        raise NotImplementedError

    def update(self, state):
        raise NotImplementedError


class CurvatureFeature(KinematicFeature):
    """
    Центр кривизны + окружность радиуса, корректно ориентированная
    в нормальной плоскости (T-N plane).
    """

    def __init__(self, max_radius=10.0, color="yellow", opacity=0.35):
        self.max_radius = max_radius
        self.color = color
        self.opacity = opacity

        self.center_actor = None
        self.circle_actor = None

    def initialize(self, plotter):

        # Сфера центра кривизны
        self.center_actor = plotter.add_mesh(
            pv.Sphere(radius=0.08),
            color=self.color,
        )
        self.center_actor.visibility = False

        # Пустой круг — будем обновлять геометрию
        dummy_circle = pv.Circle(radius=1.0)
        self.circle_actor = plotter.add_mesh(
            dummy_circle,
            color=self.color,
            opacity=self.opacity,
        )
        self.circle_actor.visibility = False

    def update(self, state):

        pos = state["pos"]
        T = state["T"]
        N = state["N"]
        B = state["B"]
        R = state["radius"]

        print(f"[Curv] seg={state['seg']} R={R:.3f} Curv={state['curvature']:.3f}")
        # --- Прямая линия → R → ∞ ---
        if np.isinf(R) or R > self.max_radius:
            self.center_actor.visibility = False
            self.circle_actor.visibility = False
            return

        # ===========================================================
        # 1) Центр кривизны C = pos + N * R
        # ===========================================================
        C = pos + N * R

        self.center_actor.SetPosition(C)
        self.center_actor.visibility = True

        # ===========================================================
        # 2) Построение окружности правильно ориентированной
        #
        #  pv.Circle() лежит в плоскости XY, нормаль = +Z.
        #
        #  Хотим, чтобы:
        #    нормаль круга   = B
        #    "вправо" круга  = N
        #    "вверх" круга   = -T       ← это важно!
        # ===========================================================

        circle = pv.Circle(radius=R, resolution=128)

        right = N
        up = -T
        normal = B

        M = np.eye(4)
        M[:3, :3] = np.column_stack([right, up, normal])
        M[:3, 3] = C  # позиция центра круга

        transformed_circle = circle.transform(M, inplace=False)

        # обновляем геометрию
        self.circle_actor.mapper.SetInputData(transformed_circle)
        self.circle_actor.visibility = True
