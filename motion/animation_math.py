import numpy as np
from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
)
from motion.interpolation_strategies import StrategyRegistry


class TrajectoryAnimator:
    """Вычисление состояния объекта в момент времени анимации"""

    def __init__(self, trajectory):
        self.trajectory = trajectory
        self.cum_len = cumulative_lengths(trajectory)
        self.total_len = polyline_length(trajectory)

        # Импортируем для использования в стратегиях
        from motion.trajectory import interpolate_orientation
        self.directions_seg = interpolate_orientation(trajectory)

    def get_state(self, t: float, interpolation_type: str, orientation_type: str) -> dict:
        """
        Args:
            t: параметр времени [0, 1]
            interpolation_type: название стратегии позиции
            orientation_type: название стратегии ориентации
        """
        # Получаем стратегии из реестра
        pos_strategy = StrategyRegistry.get_position_strategy(interpolation_type)
        orient_strategy = StrategyRegistry.get_orientation_strategy(orientation_type)

        # Вычисляем позицию
        pos = pos_strategy(self.trajectory, t)

        # Вычисляем направление
        # Передаём дополнительные параметры, которые могут понадобиться стратегии
        direction = orient_strategy(
            self.trajectory,
            t,
            directions_seg=self.directions_seg,
            cum_len=self.cum_len,
            total_len=self.total_len
        )
        direction = direction / np.linalg.norm(direction)

        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        return {
            "position": pos,
            "yaw": yaw,
            "direction": direction
        }

    # Для обратной совместимости
    def get_state_by_parameter(self, t: float) -> dict:
        return self.get_state(t, "index", "index")

    def get_state_by_length(self, t: float) -> dict:
        return self.get_state(t, "length", "length")