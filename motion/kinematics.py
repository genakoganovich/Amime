import numpy as np
from scipy.interpolate import CubicSpline

# импорт ТОЛЬКО того, что уже реализовано
from motion.trajectory import (
    polyline_length,
    cumulative_lengths,
    interpolate_position,
    interpolate_position_by_length,
    interpolate_orientation,
    interpolate_orientation_by_length,
)


# ============================================================
# FRENÉT–SERRET FRAME (T, N, B)
# ============================================================

def frenet_frame(points: np.ndarray):
    """
    Возвращает три массива одинаковой длины:
        T — касательные векторы
        N — нормали
        B — бинормали
    """

    # Касательная T (уже вычислена в trajectory)
    T = interpolate_orientation(points)  # Nx3

    # Производная T по индексу
    dT = np.diff(T, axis=0)
    norms = np.linalg.norm(dT, axis=1, keepdims=True)

    # Нормаль N
    N = np.zeros_like(T)
    N[:-1] = dT / np.where(norms == 0, 1, norms)

    # нормировка N
    norms2 = np.linalg.norm(N, axis=1, keepdims=True)
    N = N / np.where(norms2 == 0, 1, norms2)

    # бинормаль B = T × N
    B = np.cross(T, N)

    return T, N, B


# ============================================================
# CURVATURE AND RADIUS OF CURVATURE
# ============================================================

def curvature(points: np.ndarray) -> np.ndarray:
    """
    Кривизна κ(s) на дискретной траектории.
    """
    v1 = np.diff(points, axis=0)
    v2 = np.diff(v1, axis=0)

    num = np.linalg.norm(np.cross(v1[:-1], v1[1:]), axis=1)
    den = np.linalg.norm(v1[:-1], axis=1)**3

    k = np.zeros(len(points))
    k[1:-1] = num / np.where(den == 0, 1, den)
    return k


def radius_of_curvature(points: np.ndarray):
    """
    R = 1 / κ
    """
    k = curvature(points)
    R = np.zeros_like(k)
    R[k != 0] = 1.0 / k[k != 0]
    R[k == 0] = np.inf
    return R


# ============================================================
# KINEMATIC PROFILES: time → length s(t)
# ============================================================

def s_curve(t, T):
    """
    S‑кривая (smoothstep) для плавного старта/остановки.
    """
    x = t / T
    return x * x * (3 - 2 * x)


def constant_speed(total_length, t, T):
    """
    Равномерное движение.
    """
    return min(total_length, total_length * t / T)


def accel_decel(total_length, t, T, v_max=1.0, a=1.0):
    """
    Разгон → равномерно → торможение.
    """
    t_acc = v_max / a
    s_acc = 0.5 * a * t_acc**2

    if 2 * s_acc > total_length:
        # траектория слишком короткая — треугольный профиль
        t_peak = np.sqrt(total_length / a)
        if t < t_peak:
            return 0.5 * a * t**2
        else:
            dt = t - t_peak
            v_peak = a * t_peak
            return total_length - 0.5 * a * dt**2

    # разгон
    if t < t_acc:
        return 0.5 * a * t**2

    # равномерная скорость
    s1 = s_acc
    t1 = t - t_acc
    s2 = min(v_max * t1, total_length - 2 * s_acc)

    return s1 + s2


# ============================================================
# VELOCITY & ACCELERATION ALONG TRAJECTORY
# ============================================================

def tangent_velocity(points, s, ds=1e-4):
    """
    dP/ds — производная позиции по длине пути.
    """
    p1 = interpolate_position_by_length(points, s)
    p2 = interpolate_position_by_length(points, s + ds)
    return (p2 - p1) / ds


def tangent_acceleration(points, s, ds=1e-4):
    """
    d²P/ds² — вторая производная по длине пути.
    """
    v1 = tangent_velocity(points, s, ds)
    v2 = tangent_velocity(points, s + ds, ds)
    return (v2 - v1) / ds


# ============================================================
# SPLINE TRAJECTORIES
# ============================================================

def cubic_spline_trajectory(points: np.ndarray):
    """
    Возвращает три CubicSpline — по x, y, z.
    """
    t = np.linspace(0, 1, len(points))
    return (
        CubicSpline(t, points[:, 0]),
        CubicSpline(t, points[:, 1]),
        CubicSpline(t, points[:, 2]),
    )


def spline_position(splines, t):
    """
    Возвращает 3D точку на сплайне.
    """
    sx, sy, sz = splines
    return np.array([sx(t), sy(t), sz(t)])