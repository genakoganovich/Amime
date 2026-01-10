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
        """
        Args:
            global_params: глобальные параметры (SPHERE_RADIUS, ARROW_SCALE и т.д.)
        """
        self.global_params = global_params

    def create_sphere(self, name: str, color: str, **kwargs) -> ActorConfig:
        """
        Создать конфиг сферы

        Args:
            name: имя объекта
            color: цвет
            **kwargs: доп. параметры (radius, theta_resolution, phi_resolution)
        """
        radius = kwargs.get("radius", self.global_params.get("sphere_radius", 0.1))

        return ActorConfig(
            name=name,
            color=color,
            mesh_type="sphere",
            mesh_params={
                "radius": radius,
                "theta_resolution": kwargs.get("theta_resolution", 10),
                "phi_resolution": kwargs.get("phi_resolution", 10),
            }
        )

    def create_arrow(self, name: str, color: str, **kwargs) -> ActorConfig:
        """
        Создать конфиг стрелки

        Args:
            name: имя объекта
            color: цвет
            **kwargs: доп. параметры (direction, scale)
        """
        arrow_scale = kwargs.get("scale", self.global_params.get("arrow_scale", 1.0))

        return ActorConfig(
            name=name,
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
        """
        Args:
            global_params: глобальные параметры (SPHERE_RADIUS, ARROW_SCALE и т.д.)
        """
        self.global_params = global_params
        self.factory = ActorConfigFactory(global_params)
        self.groups: Dict[str, ActorGroupConfig] = {}

    def add_group(self, group_name: str, actors: List[ActorConfig]) -> "ActorConfigurationBuilder":
        """
        Добавить группу объектов

        Args:
            group_name: название группы
            actors: список конфигов объектов

        Returns:
            self для chaining
        """
        self.groups[group_name] = ActorGroupConfig(name=group_name, actors=actors)
        return self

    def add_sphere_group(self, group_name: str, actor_name: str,
                         color: str, **kwargs) -> "ActorConfigurationBuilder":
        """
        Добавить группу с одной сферой

        Args:
            group_name: название группы
            actor_name: имя объекта
            color: цвет
            **kwargs: доп. параметры для сферы

        Returns:
            self для chaining
        """
        actor = self.factory.create_sphere(actor_name, color, **kwargs)
        return self.add_group(group_name, [actor])

    def add_arrow_group(self, group_name: str, actor_name: str,
                        color: str, **kwargs) -> "ActorConfigurationBuilder":
        """
        Добавить группу со стрелкой

        Args:
            group_name: название группы
            actor_name: имя объекта
            color: цвет
            **kwargs: доп. параметры для стрелки

        Returns:
            self для chaining
        """
        actor = self.factory.create_arrow(actor_name, color, **kwargs)
        return self.add_group(group_name, [actor])

    def add_sphere_and_arrow_group(self, group_name: str,
                                   color: str, **kwargs) -> "ActorConfigurationBuilder":
        """
        Добавить группу со сферой и стрелкой

        Args:
            group_name: название группы
            color: цвет
            **kwargs: доп. параметры

        Returns:
            self для chaining
        """
        sphere = self.factory.create_sphere(f"{group_name}_sphere", color, **kwargs)
        arrow = self.factory.create_arrow(f"{group_name}_arrow", color, **kwargs)
        return self.add_group(group_name, [sphere, arrow])

    def get_all_groups(self) -> Dict[str, ActorGroupConfig]:
        """Получить все группы"""
        return self.groups

    def get_group(self, group_name: str) -> ActorGroupConfig:
        """Получить одну группу"""
        return self.groups[group_name]


class DefaultActorConfiguration(ActorConfigurationBuilder):
    """Дефолтная конфигурация - два метода интерполяции со сфера + стрелка"""

    def __init__(self, global_params: Dict):
        super().__init__(global_params)
        self._setup_default_config()

    def _setup_default_config(self):
        """Настроить дефолтную конфигурацию"""
        # Метод 1: интерполяция по параметру (сфера + стрелка)
        self.add_sphere_and_arrow_group("method_1", color="red")

        # Метод 2: интерполяция по длине дуги (сфера + стрелка)
        self.add_sphere_and_arrow_group("method_2", color="cyan")