import pyvista as pv
import numpy as np
from dataclasses import dataclass


@dataclass
class MeshActor:
    """Обертка над PyVista mesh для удобства"""
    mesh: pv.Actor
    color: str


class TrajectoryVisualizer:
    """Управление сценой и отрисовкой"""

    def __init__(self, trajectory, config):
        self.trajectory = trajectory
        self.config = config
        self.plotter = pv.Plotter()
        self._setup_scene()
        self._create_actors()

    def _setup_scene(self):
        """Инициализация сцены"""
        self.plotter.set_background("black")
        self.plotter.add_mesh(
            pv.lines_from_points(self.trajectory),
            color="yellow",
            line_width=3
        )

    def _create_actors(self):
        """Создание объектов сцены"""
        radius = self.config["sphere_radius"]
        scale = self.config["arrow_scale"]

        # Метод 1: по параметру
        self.actor_seg = {
            "sphere": MeshActor(
                self.plotter.add_mesh(
                    pv.Sphere(radius=radius),
                    color="red"
                ),
                "red"
            ),
            "arrow": MeshActor(
                self.plotter.add_mesh(
                    pv.Arrow(direction=(1, 0, 0), scale=scale),
                    color="red"
                ),
                "red"
            )
        }

        # Метод 2: по длине дуги
        self.actor_len = {
            "sphere": MeshActor(
                self.plotter.add_mesh(
                    pv.Sphere(radius=radius),
                    color="cyan"
                ),
                "cyan"
            ),
            "arrow": MeshActor(
                self.plotter.add_mesh(
                    pv.Arrow(direction=(1, 0, 0), scale=scale),
                    color="cyan"
                ),
                "cyan"
            )
        }

    def update_actor(self, actors: dict, state: dict):
        """Обновить положение и ориентацию объекта"""
        actors["sphere"].mesh.SetPosition(state["position"])
        actors["arrow"].mesh.SetPosition(state["position"])
        actors["arrow"].mesh.SetOrientation(0, 0, state["yaw"])

    def show(self):
        """Запустить интерактивную сцену"""
        self.plotter.show(interactive_update=True)

    def update(self):
        """Обновить кадр"""
        self.plotter.update()

    def render_frame(self, state_seg: dict, state_len: dict):
        """Отрисовать один кадр с двумя состояниями"""
        self.update_actor(self.actor_seg, state_seg)
        self.update_actor(self.actor_len, state_len)
        self.update()