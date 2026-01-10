import pyvista as pv
from dataclasses import dataclass
from typing import List, Dict, Any, Callable
from motion.mesh_factory import MeshFactory


@dataclass
class MeshActor:
    """Обертка над PyVista mesh"""
    mesh: pv.Actor
    color: str


@dataclass
class ActorConfig:
    """Конфиг для одного объекта на сцене"""
    name: str
    color: str
    mesh_type: str  # "sphere", "arrow", etc.
    mesh_params: Dict[str, Any]  # {"radius": 0.1} или {"scale": 1.0}


@dataclass
class ActorState:
    """Состояние актора (позиция + ориентация)"""
    position: tuple
    yaw: float


class TrajectoryVisualizer:
    """Чистая визуализация - получает данные извне"""

    def __init__(self, trajectory, global_config: Dict[str, Any],
                 mesh_factory: MeshFactory = None):
        """
        Args:
            trajectory: траектория для отрисовки
            global_config: глобальные параметры (радиус, масштаб и т.д.)
            mesh_factory: фабрика для создания mesh объектов (опционально)
        """
        self.trajectory = trajectory
        self.global_config = global_config
        self.mesh_factory = mesh_factory or MeshFactory()

        self.plotter = pv.Plotter()
        self._setup_scene()

        self.actors: Dict[str, Dict[str, MeshActor]] = {}

        # Словарь для сохранения функций-провайдеров состояния
        # ключ: (group_name, actor_name), значение: callable() -> ActorState
        self.state_providers: Dict[tuple, Callable[[], ActorState]] = {}

    def _setup_scene(self):
        """Инициализация сцены"""
        self.plotter.set_background("black")
        self.plotter.add_mesh(
            pv.lines_from_points(self.trajectory),
            color="yellow",
            line_width=3
        )

    def add_actor_group(self, group_name: str, configs: List[ActorConfig]):
        """
        Добавить группу объектов на сцену

        Args:
            group_name: название группы (например, "method_1", "method_2")
            configs: список ActorConfig для объектов в группе
        """
        self.actors[group_name] = {}

        for config in configs:
            mesh = self.mesh_factory.create(config.mesh_type, config.mesh_params)
            actor = self.plotter.add_mesh(mesh, color=config.color)

            self.actors[group_name][config.name] = MeshActor(actor, config.color)

    def register_state_provider(self, group_name: str, actor_name: str,
                                provider: Callable[[], ActorState]):
        """
        Зарегистрировать функцию-провайдер состояния для актора

        Args:
            group_name: название группы
            actor_name: имя актора
            provider: функция которая возвращает ActorState
        """
        key = (group_name, actor_name)
        self.state_providers[key] = provider

    def update_actor_state(self, group_name: str, actor_name: str, state: Dict[str, Any]):
        """Обновить состояние объекта (позиция + ориентация)"""
        self.update_actor_position(group_name, actor_name, state["position"])
        self.update_actor_orientation(group_name, actor_name, state["yaw"])

    def update_actor_position(self, group_name: str, actor_name: str, position):
        """Обновить позицию объекта"""
        actor = self.actors[group_name][actor_name].mesh
        actor.SetPosition(position)

    def update_actor_orientation(self, group_name: str, actor_name: str, yaw: float):
        """Обновить ориентацию объекта"""
        actor = self.actors[group_name][actor_name].mesh
        actor.SetOrientation(0, 0, yaw)

    def update_all_actors(self):
        """
        Обновить состояние всех зарегистрированных акторов
        Берет состояние от провайдеров
        """
        for (group_name, actor_name), provider in self.state_providers.items():
            state = provider()
            self.update_actor_position(group_name, actor_name, state.position)
            self.update_actor_orientation(group_name, actor_name, state.yaw)

    def show(self):
        """Запустить интерактивную сцену"""
        self.plotter.show(interactive_update=True)

    def update(self):
        """Обновить кадр"""
        self.plotter.update()