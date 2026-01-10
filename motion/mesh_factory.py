import pyvista as pv
from typing import Dict, Any


class MeshFactory:
    """Фабрика для создания PyVista mesh объектов"""

    def __init__(self):
        self._creators = {
            "sphere": self._create_sphere,
            "arrow": self._create_arrow,
        }

    def create(self, mesh_type: str, params: Dict[str, Any]) -> pv.DataObject:
        """
        Создать mesh объект

        Args:
            mesh_type: тип объекта ("sphere", "arrow", etc.)
            params: параметры для объекта

        Returns:
            pv.DataObject (Sphere, Arrow, etc.)

        Raises:
            ValueError: если тип не поддерживается
        """
        creator = self._creators.get(mesh_type)

        if creator is None:
            raise ValueError(
                f"Unknown mesh type: {mesh_type}. "
                f"Available: {list(self._creators.keys())}"
            )

        return creator(params)

    @staticmethod
    def _create_sphere(params: Dict[str, Any]) -> pv.Sphere:
        """Создать сферу"""
        return pv.Sphere(
            radius=params.get("radius", 0.1),
            theta_resolution=params.get("theta_resolution", 10),
            phi_resolution=params.get("phi_resolution", 10)
        )

    @staticmethod
    def _create_arrow(params: Dict[str, Any]) -> pv.Arrow:
        """Создать стрелку"""
        return pv.Arrow(
            direction=params.get("direction", (1, 0, 0)),
            scale=params.get("scale", 1.0)
        )

    def register_creator(self, mesh_type: str, creator_func):
        """
        Зарегистрировать новый тип mesh

        Args:
            mesh_type: название типа
            creator_func: функция(params) -> pv.DataObject
        """
        self._creators[mesh_type] = creator_func

    def get_available_types(self) -> list:
        """Получить список доступных типов mesh"""
        return list(self._creators.keys())