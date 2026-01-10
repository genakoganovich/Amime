from typing import Dict, Tuple
from motion.animation_math import TrajectoryAnimator
from motion.visualization import TrajectoryVisualizer, ActorState
from motion.mesh_factory import MeshFactory
from motion.actor_loader import ActorLoader


class AnimationSetup:
    """Инициализация и подготовка анимации"""

    def __init__(self, trajectory, global_config: Dict, config_file: str):
        """
        Args:
            trajectory: траектория
            global_config: глобальные параметры (radius, scale)
            config_file: путь к JSON файлу с конфигурацией акторов
        """
        self.trajectory = trajectory
        self.global_config = global_config
        self.config_file = config_file

        self.animator = None
        self.visualizer = None
        self.animation_config = None

    def setup(self) -> Tuple[TrajectoryVisualizer, TrajectoryAnimator, Dict]:
        """
        Полная инициализация

        Returns:
            (visualizer, animator, animation_config)
        """
        # Инициализируем animator
        self.animator = TrajectoryAnimator(self.trajectory)

        # Создаем visualizer
        mesh_factory = MeshFactory()
        self.visualizer = TrajectoryVisualizer(
            self.trajectory,
            self.global_config,
            mesh_factory
        )

        # Загружаем конфигурацию из файла
        self._load_actors_config()

        # Добавляем акторов на сцену
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

        def make_provider(method):
            """Создать провайдер для конкретного метода"""

            def provider():
                if method == "parameter":
                    state = self.animator.get_state_by_parameter(self._current_t["value"])
                else:  # length
                    state = self.animator.get_state_by_length(self._current_t["value"])

                return ActorState(
                    position=list(state["position"]),
                    yaw=state["yaw"]
                )

            return provider

        # Добавляем каждого актора
        for actor_name, actor in self.actor_config.get_all_actors().items():
            method = self.animation_config[actor_name]

            self.visualizer.add_actor_with_provider(
                actor_name,
                actor.visuals,
                make_provider(method)
            )

    def get_current_t_dict(self) -> Dict:
        """Получить словарь для хранения текущего времени"""
        if not hasattr(self, '_current_t'):
            self._current_t = {"value": 0.0}
        return self._current_t