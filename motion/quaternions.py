import numpy as np
from scipy.spatial.transform import Rotation as R, Slerp


# ============================================================
# Базовые функции для кватернионов
# ============================================================

def quat_from_direction(direction, up=np.array([0, 0, 1.0])):
    """
    Создаёт кватернион, который ориентирует ось Z вдоль direction.
    Используется для ориентации камеры, стрелок и объектов.
    """
    direction = direction / np.linalg.norm(direction)

    # Строим ортонормальный базис (right, up2, forward)
    right = np.cross(up, direction)
    if np.linalg.norm(right) < 1e-6:
        # направление коллинеарно "up": выбираем произвольную ось
        right = np.array([1, 0, 0])

    right /= np.linalg.norm(right)
    up2 = np.cross(direction, right)

    rot_matrix = np.vstack([right, up2, direction]).T
    return R.from_matrix(rot_matrix)


def quat_to_matrix(quat: R) -> np.ndarray:
    """
    Конвертация Rotation → 3x3 матрица.
    """
    return quat.as_matrix()


def quat_apply(quat: R, vec: np.ndarray) -> np.ndarray:
    """
    Применяет кватернион к вектору.
    """
    return quat.apply(vec)


# ============================================================
# SLERP — сферическая интерполяция между кватернионами
# ============================================================

def quat_slerp(q0: R, q1: R, t: float) -> R:
    """
    Безопасный SLERP, совместимый со старыми SciPy.
    q0, q1 — Rotation
    t — float от 0 до 1
    """
    key_times = [0, 1]
    key_rots = R.from_quat([q0.as_quat(), q1.as_quat()])
    slerp = Slerp(key_times, key_rots)
    return slerp([t])[0]


# ============================================================
# Дополнительные утилиты
# ============================================================

def look_at_rotation(position: np.ndarray, target: np.ndarray, up=np.array([0, 0, 1.0])) -> R:
    """
    Строит ориентацию (кватернион), чтобы "смотреть" из позиции position на target.
    """
    direction = target - position
    direction /= np.linalg.norm(direction)
    return quat_from_direction(direction, up)


def smooth_lerp(a: np.ndarray, b: np.ndarray, factor: float) -> np.ndarray:
    """
    Плавная линейная интерполяция для позиций камер.
    """
    return a * (1 - factor) + b * factor


def smoothstep(t: float) -> float:
    """
    Плавное сглаживание (ease-in-out) для параметров движения.
    """
    return t * t * (3 - 2 * t)
