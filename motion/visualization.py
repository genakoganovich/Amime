import pyvista as pv
from dataclasses import dataclass
from typing import Dict, Any, Callable, List
from motion.mesh_factory import MeshFactory


@dataclass
class MeshActor:
    """Визуальный элемент на сцене"""
    mesh: pv.Actor
    color: str


@dataclass
class ActorConfig:
    """Конфиг для одного визуального элемента"""
    name: str
    color: str
    mesh_type: str
    mesh_params: Dict[str, Any]


@dataclass
class ActorState:
    """Состояние актора"""
    position: tuple
    yaw: float

@dataclass
class ActorVisuals:
    """Визуалы актора + его провайдер состояния"""
    name: str
    visuals: List[str]  # имена визуальных элементов
    state_provider: Callable[[], ActorState]

class TrajectoryVisualizer:
    """Визуализация траектории"""

    def __init__(self, trajectory, global_config: Dict[str, Any],
                 mesh_factory: MeshFactory = None):
        self.trajectory = trajectory
        self.global_config = global_config
        self.mesh_factory = mesh_factory or MeshFactory()

        self.plotter = pv.Plotter()
        self._setup_scene()

        # Визуальные элементы на сцене (sphere, arrow и т.д.)
        self.visuals: Dict[str, MeshActor] = {}
        self.actors: Dict[str, ActorVisuals] = {}  # actor_name -> визуалы + провайдер

        # Вместо state_providers по имени актора,
        # используем список провайдеров
        self.state_providers: List[tuple] = []  # (actor_name, provider)



    def _setup_scene(self):
        """Инициализация сцены"""
        self.plotter.set_background("black")
        self.plotter.add_mesh(
            pv.lines_from_points(self.trajectory),
            color="yellow",
            line_width=3
        )

    def add_actor(self, actor_name: str, visual_configs: List[ActorConfig]):
        """Добавить актора на сцену"""
        for config in visual_configs:
            mesh = self.mesh_factory.create(config.mesh_type, config.mesh_params)
            visual = self.plotter.add_mesh(mesh, color=config.color)

            self.visuals[config.name] = MeshActor(visual, config.color)


    def add_actor_with_provider(self, actor_name: str,
                                visual_configs: List[ActorConfig],
                                state_provider: Callable[[], ActorState]):
        """
        Добавить актора с его визуалами и провайдером состояния
        """
        visual_names = []

        for config in visual_configs:
            mesh = self.mesh_factory.create(config.mesh_type, config.mesh_params)
            visual = self.plotter.add_mesh(mesh, color=config.color)

            self.visuals[config.name] = MeshActor(visual, config.color)
            visual_names.append(config.name)

        self.actors[actor_name] = ActorVisuals(
            name=actor_name,
            visuals=visual_names,
            state_provider=state_provider
        )

    def update_all_actors(self):
        """Обновить состояние всех акторов"""
        for actor in self.actors.values():
            state = actor.state_provider()

            # Обновляем все визуалы этого актора
            for visual_name in actor.visuals:
                visual = self.visuals[visual_name].mesh
                visual.SetPosition(state.position)
                visual.SetOrientation(0, 0, state.yaw)

    def show(self):
        """Запустить интерактивную сцену"""
        self.plotter.show(interactive_update=True)

    def update(self):
        """Обновить кадр"""
        self.plotter.update()