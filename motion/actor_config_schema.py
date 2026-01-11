from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ActorConfigRow:
    """Строка конфигурации актора с поддержкой произвольных параметров"""
    actor_type: str
    color: str
    interpolation_type: str
    orientation_type: str
    extra: Dict[str, Any] = None  # Для будущих параметров

    def __post_init__(self):
        if self.extra is None:
            self.extra = {}

    def get(self, key: str, default=None):
        """Получить значение параметра (в том числе из extra)"""
        if hasattr(self, key):
            return getattr(self, key)
        return self.extra.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь"""
        return {
            'actor_type': self.actor_type,
            'color': self.color,
            'interpolation_type': self.interpolation_type,
            'orientation_type': self.orientation_type,
            **self.extra
        }