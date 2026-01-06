import numpy as np


# ============================================================
# VECTOR → ORIENTATION HELPERS
# ============================================================

def direction_to_euler(vec: np.ndarray):
    """
    Convert a direction vector (dx,dy,dz) into Euler angles
    (pitch, yaw, roll) suitable for PyVista Actor.SetOrientation.

    PyVista convention:
        yaw   — rotate around Z axis
        pitch — rotate around Y axis
        roll  — rotate around X axis
    """
    dx, dy, dz = vec

    # yaw — angle around Z
    yaw = np.degrees(np.arctan2(dy, dx))

    # pitch — angle around Y
    pitch = np.degrees(np.arctan2(dz, np.hypot(dx, dy)))

    # roll — not used for Frenet frame
    roll = 0.0

    return pitch, yaw, roll


def direction_to_rotation_matrix(vec: np.ndarray):
    """
    Return 3×3 rotation matrix whose Z-axis points along vec.
    This is useful when working with PyVista transforms.
    """
    v = vec / np.linalg.norm(vec)

    # choose a helper vector to avoid degenerate cases
    if abs(v[2]) < 0.99:
        helper = np.array([0, 0, 1])
    else:
        helper = np.array([1, 0, 0])

    right = np.cross(helper, v)
    right /= np.linalg.norm(right)

    up = np.cross(v, right)

    # rotation matrix: columns = basis vectors
    return np.column_stack([right, up, v])


# ============================================================
# VISUAL ACTOR HELPERS
# ============================================================

def apply_direction_to_actor(actor, direction: np.ndarray, scale=1.0):
    """
    Set actor orientation & scale using a direction vector.
    Uses Euler internally.
    """
    pitch, yaw, roll = direction_to_euler(direction)
    actor.SetOrientation(pitch, yaw, roll)
    actor.SetScale(scale)


def move_actor(actor, position: np.ndarray):
    """ Move a PyVista Actor to the given 3D position. """
    actor.SetPosition(position)


# ============================================================
# COLOR MAP HELPERS
# ============================================================

def scalar_to_color(value, min_val, max_val):
    """
    Map scalar value to an RGB color smoothly.
    Useful for colorizing curvature, speed, acceleration, etc.
    """
    if max_val == min_val:
        alpha = 0.5
    else:
        alpha = (value - min_val) / (max_val - min_val)
    alpha = np.clip(alpha, 0, 1)

    # simple gradient: blue → green → yellow → red
    r = alpha
    g = 1.0 - abs(alpha - 0.5) * 2
    b = 1.0 - alpha

    return (r, g, b)