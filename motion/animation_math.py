import numpy as np
from motion.trajectory import (
    cumulative_lengths,
    polyline_length,
    interpolate_position,
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
)


class TrajectoryAnimator:
    """Вычисление состояния объекта в момент времени анимации"""

    def __init__(self, trajectory):
        self.trajectory = trajectory
        self.cum_len = cumulative_lengths(trajectory)
        self.total_len = polyline_length(trajectory)
        self.directions_seg = interpolate_orientation(trajectory)

    def get_state(self, t: float, interpolation_type: str, orientation_type: str) -> dict:
        """
        Получить состояние с гибким выбором методов интерполяции

        Args:
            t: параметр времени [0, 1]
            interpolation_type: "index" или "length"
            orientation_type: "index" или "length"
        """
        # Выбираем метод интерполяции позиции
        if interpolation_type == "index":
            pos = interpolate_position(
                self.trajectory,
                t * (len(self.trajectory) - 1)
            )
        elif interpolation_type == "length":
            pos = interpolate_position_by_length(
                self.trajectory,
                t * self.total_len
            )
        else:
            raise ValueError(f"Unknown interpolation_type: {interpolation_type}")

        # Выбираем метод интерполяции ориентации
        if orientation_type == "index":
            seg_idx = int(np.clip(
                int(t * (len(self.trajectory) - 1)),
                0,
                len(self.directions_seg) - 1
            ))
            direction = self.directions_seg[seg_idx]
        elif orientation_type == "length":
            direction = interpolate_orientation_by_length(
                self.cum_len,
                self.directions_seg,
                t * self.total_len
            )
        else:
            raise ValueError(f"Unknown orientation_type: {orientation_type}")

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