import numpy as np


def polyline_length(points: np.ndarray) -> float:
    diffs = np.diff(points, axis=0)
    return float(np.sum(np.linalg.norm(diffs, axis=1)))


def cumulative_lengths(points: np.ndarray) -> np.ndarray:
    diffs = np.diff(points, axis=0)
    seg_lengths = np.linalg.norm(diffs, axis=1)
    return np.concatenate([[0.0], np.cumsum(seg_lengths)])


def interpolate_position(points: np.ndarray, t: float) -> np.ndarray:
    """
    Интерполирует позицию вдоль траектории.

    Args:
        points: np.ndarray, shape (N, 3)
        t: float, индекс вдоль траектории (0..N-1)

    Returns:
        np.ndarray, shape (3,) — интерполированная позиция
    """
    if t <= 0:
        return points[0].copy()
    elif t >= len(points) - 1:
        return points[-1].copy()

    i = int(np.floor(t))  # левая точка
    frac = t - i  # доля между i и i+1
    return points[i] + (points[i + 1] - points[i]) * frac


def interpolate_position_by_length(points: np.ndarray, s: float) -> np.ndarray:
    """
    Интерполирует позицию вдоль траектории по длине.

    Args:
        points: np.ndarray, shape (N, 3)
        s: float, расстояние вдоль траектории (0..total_length)

    Returns:
        np.ndarray, shape (3,) — интерполированная позиция
    """
    cum_len = cumulative_lengths(points)
    if s <= 0:
        return points[0].copy()
    elif s >= cum_len[-1]:
        return points[-1].copy()

    # находим сегмент, в котором находится s
    idx = np.searchsorted(cum_len, s) - 1
    frac = (s - cum_len[idx]) / (cum_len[idx + 1] - cum_len[idx])
    return points[idx] + (points[idx + 1] - points[idx]) * frac

def interpolate_orientation(points: np.ndarray) -> np.ndarray:
    """
    Вычисляет направление движения вдоль траектории для каждой точки.
    Возвращает массив Nx3 с единичными векторами направления.
    Последний вектор повторяет предпоследний.
    """
    directions = np.diff(points, axis=0)
    norms = np.linalg.norm(directions, axis=1, keepdims=True)
    directions = directions / norms
    # Добавляем последний вектор
    directions = np.vstack([directions, directions[-1]])
    return directions



def interpolate_orientation_by_length(cum_lengths, directions, s):
    """
    cum_lengths: (N,) накопленные длины
    directions: (N,3) направления (из interpolate_orientation)
    s: длина вдоль траектории
    """

    if s <= 0:
        return directions[0]

    if s >= cum_lengths[-1]:
        return directions[-1]

    idx = np.searchsorted(cum_lengths, s) - 1
    idx = np.clip(idx, 0, len(directions) - 2)

    # параметр внутри сегмента
    t = (s - cum_lengths[idx]) / (cum_lengths[idx + 1] - cum_lengths[idx])

    # 🔥 ВОТ ГЛАВНОЕ ОТЛИЧИЕ
    d = (1 - t) * directions[idx] + t * directions[idx + 1]
    return d / np.linalg.norm(d)
