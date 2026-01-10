from typing import Dict, List
from dataclasses import dataclass
from motion.visualization import ActorConfig


@dataclass
class ActorGroupConfig:
    """Конфиг группы объектов"""
    name: str
    actors: List[ActorConfig]


class ActorConfigFactory:
    """Фабрика для создания конфигов отдельных объектов"""

    def __init__(self, global_params: Dict):
        self.global_params = global_params

    def create_sphere(self, actor_name: str, color: str, **kwargs) -> ActorConfig:
        """Создать конфиг сферы"""
        radius = kwargs.get("radius", self.global_params.get("sphere_radius", 0.1))

        return ActorConfig(
            name=actor_name,
            color=color,
            mesh_type="sphere",
            mesh_params={
                "radius": radius,
                "theta_resolution": kwargs.get("theta_resolution", 10),
                "phi_resolution": kwargs.get("phi_resolution", 10),
            }
        )

    def create_arrow(self, actor_name: str, color: str, **kwargs) -> ActorConfig:
        """Создать конфиг стрелки"""
        arrow_scale = kwargs.get("scale", self.global_params.get("arrow_scale", 1.0))

        return ActorConfig(
            name=actor_name,
            color=color,
            mesh_type="arrow",
            mesh_params={
                "direction": kwargs.get("direction", (1, 0, 0)),
                "scale": arrow_scale,
            }
        )


class ActorConfigurationBuilder:
    """Построитель конфигурации объектов на сцене"""

    def __init__(self, global_params: Dict):
        self.global_params = global_params
        self.factory = ActorConfigFactory(global_params)
        # Теперь это словарь акторов, не групп!
        self.actors: Dict[str, ActorConfig] = {}

    def add_sphere(self, actor_name: str, color: str, **kwargs) -> "ActorConfigurationBuilder":
        """
        Добавить одну сферу

        Args:
            actor_name: имя актора (уникальное)
            color: цвет
            **kwargs: доп. параметры (radius, etc.)

        Returns:
            self для chaining
        """
        self.actors[actor_name] = self.factory.create_sphere(actor_name, color, **kwargs)
        return self

    def add_arrow(self, actor_name: str, color: str, **kwargs) -> "ActorConfigurationBuilder":
        """
        Добавить одну стрелку

        Args:
            actor_name: имя актора (уникальное)
            color: цвет
            **kwargs: доп. параметры (scale, direction, etc.)

        Returns:
            self для chaining
        """
        self.actors[actor_name] = self.factory.create_arrow(actor_name, color, **kwargs)
        return self

    def get_all_actors(self) -> Dict[str, ActorConfig]:
        """Получить все акторы"""
        return self.actors

    def get_actor(self, actor_name: str) -> ActorConfig:
        """Получить один актор"""
        return self.actors[actor_name]


class DefaultActorConfiguration(ActorConfigurationBuilder):
    """Дефолтная конфигурация - два метода интерполяции"""

    def __init__(self, global_params: Dict):
        super().__init__(global_params)
        self._setup_default_config()

    def _setup_default_config(self):
        """Настроить дефолтную конфигурацию"""
        # Метод 1: интерполяция по параметру
        self.add_sphere("method_1_sphere", color="red")
        self.add_arrow("method_1_arrow", color="red")

        # Метод 2: интерполяция по длине дуги
        self.add_sphere("method_2_sphere", color="cyan")
        self.add_arrow("method_2_arrow", color="cyan")