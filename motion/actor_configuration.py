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

    def create_composite(self, name_prefix: str, color: str,
                         with_sphere: bool = True,
                         with_arrow: bool = True,
                         **kwargs) -> List[ActorConfig]:
        """
        Создать комбинированный набор (сфера + стрелка)

        Args:
            name_prefix: префикс для имен объектов
            color: цвет
            with_sphere: включить сферу
            with_arrow: включить стрелку
            **kwargs: доп. параметры для sphere и arrow

        Returns:
            список ActorConfig
        """
        actors = []

        if with_sphere:
            actors.append(self.create_sphere(f"{name_prefix}_sphere", color, **kwargs))

        if with_arrow:
            actors.append(self.create_arrow(f"{name_prefix}_arrow", color, **kwargs))

        return actors


class ActorConfigurationBuilder:
    """Построитель конфигурации объектов на сцене"""

    def __init__(self, global_params: Dict):
        """
        Args:
            global_params: глобальные параметры (SPHERE_RADIUS, ARROW_SCALE и т.д.)
        """
        self.global_params = global_params
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
        self.factory = ActorConfigFactory(global_params)
        self._setup_default_config()

    def _setup_default_config(self):
        """Настроить дефолтную конфигурацию"""
        # Метод 1: интерполяция по параметру
        method_1_actors = self.factory.create_composite(
            name_prefix="method_1",
            color="red"
        )
        self.add_group("method_1", method_1_actors)

        # Метод 2: интерполяция по длине дуги
        method_2_actors = self.factory.create_composite(
            name_prefix="method_2",
            color="cyan"
        )
        self.add_group("method_2", method_2_actors)