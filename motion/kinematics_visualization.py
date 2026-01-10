import numpy as np
from motion.kinematics import frenet_frame
from motion.trajectory import interpolate_position
from motion.visualization import ActorState


class KinematicsVisualizer:
    """Визуализация кинематических характеристик траектории"""

    def __init__(self, trajectory):
        """
        Args:
            trajectory: массив 3D точек
        """
        self.trajectory = trajectory
        self.T, self.N, self.B = frenet_frame(trajectory)

    def get_tangent_vector_at_parameter(self, t: float) -> ActorState:
        """
        Получить состояние для визуализации касательного вектора (T)

        Args:
            t: параметр от 0 до 1

        Returns:
            ActorState с позицией и направлением вектора T
        """
        # Позиция на траектории
        t_param = t * (len(self.trajectory) - 1)
        position = interpolate_position(self.trajectory, t_param)

        # Индекс для получения вектора T
        idx = int(np.clip(t_param, 0, len(self.T) - 1))
        tangent = self.T[idx]

        # Угол поворота для стрелки (из вектора в угол Эйлера)
        yaw = np.degrees(np.arctan2(tangent[1], tangent[0]))

        return ActorState(
            position=list(position),
            yaw=yaw
        )