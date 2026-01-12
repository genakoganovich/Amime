"""
Стратегии интерполяции позиции и ориентации.
Каждая стратегия — это функция, которая преобразует (t, trajectory) → direction_vector
"""

import numpy as np
from motion.trajectory import (
    interpolate_position,
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
    cumulative_lengths,
    polyline_length,
)

from motion.kinematics import (
    tangent_velocity,
    normal_at_length,
    normal_by_index
)


class PositionStrategies:
    """Стратегии интерполяции позиции"""

    @staticmethod
    def index(trajectory, t):
        """Интерполяция по индексу"""
        return interpolate_position(
            trajectory,
            t * (len(trajectory) - 1)
        )

    @staticmethod
    def length(trajectory, t):
        """Интерполяция по длине дуги"""
        total_len = polyline_length(trajectory)
        s = t * total_len
        return interpolate_position_by_length(trajectory, s)


class OrientationStrategies:
    """Стратегии интерполяции ориентации"""

    @staticmethod
    def index(trajectory, t, directions_seg, **kwargs):  # ← Добавьте **kwargs
        """Дискретное направление по индексу"""
        seg_idx = int(np.clip(
            int(t * (len(trajectory) - 1)),
            0,
            len(directions_seg) - 1
        ))
        return directions_seg[seg_idx]

    @staticmethod
    def length(trajectory, t, directions_seg, cum_len, total_len, **kwargs):  # ← Добавьте **kwargs
        """Дискретное направление по длине"""
        s = t * total_len
        return interpolate_orientation_by_length(
            cum_len,
            directions_seg,
            s
        )

    @staticmethod
    def tangent_velocity(trajectory, t, cum_len=None, total_len=None, **kwargs):  # ← Уже есть
        """Касательная из производной позиции по длине"""
        total_len = total_len or polyline_length(trajectory)
        s = t * total_len
        direction = tangent_velocity(trajectory, s)
        return direction / np.linalg.norm(direction)



    @staticmethod
    def frenet_normal_length(trajectory, t, cum_len=None, total_len=None, **kwargs):
        """Вектор нормали из Frenet frame"""
        total_len = total_len or polyline_length(trajectory)
        s = t * total_len

        direction = normal_at_length(trajectory, s)

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            return np.array([0.0, 0.0, 1.0])

        return direction / norm

    @staticmethod
    def frenet_normal_index(trajectory, t, **kwargs):
        """Вектор нормали из Frenet frame по индексу"""
        t_idx = t * (len(trajectory) - 1)
        direction = normal_by_index(trajectory, t_idx)

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            return np.array([0.0, 0.0, 1.0])

        return direction / norm

    @staticmethod
    def my_custom_function(trajectory, t, **kwargs):  # ← Уже есть
        """Пример вашей новой функции"""
        pass


class StrategyRegistry:
    """Реестр стратегий интерполяции"""

    _position_strategies = {
        'index': PositionStrategies.index,
        'length': PositionStrategies.length,
    }

    _orientation_strategies = {
        'index': OrientationStrategies.index,
        'length': OrientationStrategies.length,
        'tangent_velocity': OrientationStrategies.tangent_velocity,
        'frenet_normal_length': OrientationStrategies.frenet_normal_length,
        'frenet_normal_index': OrientationStrategies.frenet_normal_index,
        'my_custom_function': OrientationStrategies.my_custom_function,
    }

    @classmethod
    def register_position_strategy(cls, name: str, func):
        """Зарегистрировать новую стратегию позиции"""
        cls._position_strategies[name] = func

    @classmethod
    def register_orientation_strategy(cls, name: str, func):
        """Зарегистрировать новую стратегию ориентации"""
        cls._orientation_strategies[name] = func

    @classmethod
    def get_position_strategy(cls, name: str):
        """Получить стратегию позиции"""
        if name not in cls._position_strategies:
            raise ValueError(f"Unknown position strategy: {name}")
        return cls._position_strategies[name]

    @classmethod
    def get_orientation_strategy(cls, name: str):
        """Получить стратегию ориентации"""
        if name not in cls._orientation_strategies:
            raise ValueError(f"Unknown orientation strategy: {name}")
        return cls._orientation_strategies[name]