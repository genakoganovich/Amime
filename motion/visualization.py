import pyvista as pv
from dataclasses import dataclass
from typing import Dict, Any, Callable
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
    mesh_type: str
    mesh_params: Dict[str, Any]


@dataclass
class ActorState:
    """Состояние актора (позиция + ориентация)"""
    position: tuple
    yaw: float


class TrajectoryVisualizer:
    """Чистая визуализация - получает данные извне"""

    def __init__(self, trajectory, global_config: Dict[str, Any],
                 mesh_factory: MeshFactory = None):
        self.trajectory = trajectory
        self.global_config = global_config
        self.mesh_factory = mesh_factory or MeshFactory()

        self.plotter = pv.Plotter()
        self._setup_scene()

        # Теперь это словарь акторов, а не групп
        self.actors: Dict[str, MeshActor] = {}

        # Словарь для сохранения функций-провайдеров состояния
        # ключ: actor_name, значение: callable() -> ActorState
        self.state_providers: Dict[str, Callable[[], ActorState]] = {}

    def _setup_scene(self):
        """Инициализация сцены"""
        self.plotter.set_background("black")
        self.plotter.add_mesh(
            pv.lines_from_points(self.trajectory),
            color="yellow",
            line_width=3
        )

    def add_actor(self, config: ActorConfig):
        """
        Добавить одного актора на сцену

        Args:
            config: конфиг актора (ActorConfig)
        """
        mesh = self.mesh_factory.create(config.mesh_type, config.mesh_params)
        actor = self.plotter.add_mesh(mesh, color=config.color)
        self.actors[config.name] = MeshActor(actor, config.color)

    def register_state_provider(self, actor_name: str,
                                provider: Callable[[], ActorState]):
        """
        Зарегистрировать функцию-провайдер состояния для актора

        Args:
            actor_name: имя актора
            provider: функция которая возвращает ActorState
        """
        self.state_providers[actor_name] = provider

    def update_actor_state(self, actor_name: str, state: ActorState):
        """Обновить состояние актора"""
        actor = self.actors[actor_name].mesh
        actor.SetPosition(state.position)
        actor.SetOrientation(0, 0, state.yaw)

    def update_all_actors(self):
        """
        Обновить состояние всех зарегистрированных акторов
        Берет состояние от провайдеров
        """
        for actor_name, provider in self.state_providers.items():
            state = provider()
            self.update_actor_state(actor_name, state)

    def show(self):
        """Запустить интерактивную сцену"""
        self.plotter.show(interactive_update=True)

    def update(self):
        """Обновить кадр"""
        self.plotter.update()