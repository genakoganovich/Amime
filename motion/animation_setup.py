from typing import Dict, Tuple
from motion.animation_math import TrajectoryAnimator
from motion.visualization import TrajectoryVisualizer, ActorState
from motion.mesh_factory import MeshFactory
from motion.actor_loader import ActorLoader
from motion.kinematics_visualization import KinematicsVisualizer


class AnimationSetup:
    """Инициализация и подготовка анимации"""

    def __init__(self, trajectory, global_config: Dict, config_file: str,
                 use_kinematics: bool = False):
        self.trajectory = trajectory
        self.global_config = global_config
        self.config_file = config_file
        self.use_kinematics = use_kinematics

        self.animator = None
        self.visualizer = None
        self.kinematics_viz = None
        self.animation_config = None

    def setup(self) -> Tuple[TrajectoryVisualizer, TrajectoryAnimator, Dict]:
        """Полная инициализация"""
        self.animator = TrajectoryAnimator(self.trajectory)

        mesh_factory = MeshFactory()
        self.visualizer = TrajectoryVisualizer(
            self.trajectory,
            self.global_config,
            mesh_factory
        )

        if self.use_kinematics:
            self.kinematics_viz = KinematicsVisualizer(self.trajectory)

        self._load_actors_config()
        self._add_actors_to_scene()

        return self.visualizer, self.animator, self.animation_config

    def _load_actors_config(self):
        """Загрузить конфигурацию акторов из файла"""
        actor_config, self.animation_config = ActorLoader.load_from_json(
            self.config_file,
            self.global_config
        )
        self.actor_config = actor_config

    def _add_actors_to_scene(self):
        """Добавить акторов на сцену с провайдерами состояния"""

        def make_provider(actor_row):
            """Создать провайдер для актора с его конфигурацией"""

            def provider():
                # Получаем типы интерполяции из конфигурации
                interp_type = actor_row.interpolation_type
                orient_type = actor_row.orientation_type

                # Используем гибкий метод get_state
                state = self.animator.get_state(
                    self._current_t["value"],
                    interp_type,
                    orient_type
                )

                return ActorState(
                    position=list(state["position"]),
                    yaw=state["yaw"]
                )

            return provider

        # Добавляем каждого актора
        for actor_name, actor in self.actor_config.get_all_actors().items():
            actor_row = self.animation_config[actor_name]
            provider = make_provider(actor_row)

            self.visualizer.add_actor_with_provider(
                actor_name,
                actor.visuals,
                provider
            )

    def get_current_t_dict(self) -> Dict:
        """Получить словарь для хранения текущего времени"""
        if not hasattr(self, '_current_t'):
            self._current_t = {"value": 0.0}
        return self._current_t