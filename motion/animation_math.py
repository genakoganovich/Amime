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

    def get_state_by_parameter(self, t: float) -> dict:
        """
        Состояние по параметру t ∈ [0, 1]
        (индексная интерполяция)
        """
        pos = interpolate_position(
            self.trajectory,
            t * (len(self.trajectory) - 1)
        )

        seg_idx = int(np.clip(
            int(t * (len(self.trajectory) - 1)),
            0,
            len(self.directions_seg) - 1
        ))
        direction = self.directions_seg[seg_idx]
        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        return {
            "position": pos,
            "yaw": yaw,
            "direction": direction
        }

    def get_state_by_length(self, t: float) -> dict:
        """
        Состояние по параметру t ∈ [0, 1]
        (интерполяция по дуге)
        """
        s = t * self.total_len

        pos = interpolate_position_by_length(self.trajectory, s)
        direction = interpolate_orientation_by_length(
            self.cum_len,
            self.directions_seg[:-1],
            s
        )
        yaw = np.degrees(np.arctan2(direction[1], direction[0]))

        return {
            "position": pos,
            "yaw": yaw,
            "direction": direction
        }