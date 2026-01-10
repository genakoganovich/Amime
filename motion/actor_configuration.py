from typing import Dict, List
from dataclasses import dataclass
from motion.visualization import ActorConfig


@dataclass
class Actor:
    """Логический актор с его визуальным представлением"""
    name: str
    visuals: List[ActorConfig]  # может быть несколько визуальных элементов


class ActorConfigFactory:
    """Фабрика для создания конфигов актора"""

    def __init__(self, global_params: Dict):
        self.global_params = global_params

    def create_sphere_config(self, name: str, color: str, **kwargs) -> ActorConfig:
        """Создать конфиг сферы"""
        radius = kwargs.get("radius", self.global_params.get("sphere_radius", 0.1))

        return ActorConfig(
            name=f"{name}_sphere",
            color=color,
            mesh_type="sphere",
            mesh_params={"radius": radius}
        )

    def create_arrow_config(self, name: str, color: str, **kwargs) -> ActorConfig:
        """Создать конфиг стрелки"""
        arrow_scale = kwargs.get("scale", self.global_params.get("arrow_scale", 1.0))

        return ActorConfig(
            name=f"{name}_arrow",
            color=color,
            mesh_type="arrow",
            mesh_params={"direction": (1, 0, 0), "scale": arrow_scale}
        )


class ActorConfigurationBuilder:
    """Построитель конфигурации акторов"""

    def __init__(self, global_params: Dict):
        self.global_params = global_params
        self.factory = ActorConfigFactory(global_params)
        self.actors: Dict[str, Actor] = {}

    def add_actor(self, actor_name: str, visuals: List[ActorConfig]) -> "ActorConfigurationBuilder":
        """
        Добавить актора с его визуальным представлением

        Args:
            actor_name: имя актора
            visuals: список визуальных элементов (ActorConfig)

        Returns:
            self для chaining
        """
        self.actors[actor_name] = Actor(name=actor_name, visuals=visuals)
        return self

    def add_actor_with_sphere_and_arrow(self, actor_name: str, color: str,
                                        **kwargs) -> "ActorConfigurationBuilder":
        """
        Добавить актора со сферой и стрелкой

        Args:
            actor_name: имя актора
            color: цвет
            **kwargs: доп. параметры

        Returns:
            self для chaining
        """
        sphere = self.factory.create_sphere_config(actor_name, color, **kwargs)
        arrow = self.factory.create_arrow_config(actor_name, color, **kwargs)
        return self.add_actor(actor_name, [sphere, arrow])

    def add_actor_with_sphere_only(self, actor_name: str, color: str,
                                   **kwargs) -> "ActorConfigurationBuilder":
        """Добавить актора только со сферой"""
        sphere = self.factory.create_sphere_config(actor_name, color, **kwargs)
        return self.add_actor(actor_name, [sphere])

    def add_actor_with_arrow_only(self, actor_name: str, color: str,
                                  **kwargs) -> "ActorConfigurationBuilder":
        """Добавить актора только со стрелкой"""
        arrow = self.factory.create_arrow_config(actor_name, color, **kwargs)
        return self.add_actor(actor_name, [arrow])

    def get_all_actors(self) -> Dict[str, Actor]:
        """Получить всех акторов"""
        return self.actors

    def get_actor(self, actor_name: str) -> Actor:
        """Получить одного актора"""
        return self.actors[actor_name]


class DefaultActorConfiguration(ActorConfigurationBuilder):
    """Дефолтная конфигурация - два актора"""

    def __init__(self, global_params: Dict):
        super().__init__(global_params)
        self._setup_default_config()

    def _setup_default_config(self):
        """Настроить дефолтную конфигурацию"""
        # Актор 1: интерполяция по параметру (со сферой и стрелкой)
        self.add_actor_with_sphere_and_arrow("method_1", color="red")

        # Актор 2: интерполяция по длине дуги (со сферой и стрелкой)
        self.add_actor_with_sphere_and_arrow("method_2", color="cyan")