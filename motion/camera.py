import numpy as np

def camera_frame_target(plotter, target_pos, distance=1.0, height=0.4, padding=1.3):
    """
    Универсальный авто‑фрейминг камеры.
    100% совместим со всеми версиями PyVista/VTK.
    """

    cam = plotter.camera

    # ALWAYS CONVERT to numpy array (critical!)
    cam_pos = np.array(cam.position, dtype=float).reshape(3)
    cam_focal = np.array(cam.focal_point, dtype=float).reshape(3)
    target_pos = np.array(target_pos, dtype=float).reshape(3)

    # backward vector (camera → target)
    backward = cam_pos - cam_focal
    norm = np.linalg.norm(backward)

    if norm < 1e-6:
        backward = np.array([0.0, -1.0, 0.0])
    else:
        backward /= norm

    # new camera position
    new_pos = (
        target_pos
        + backward * distance * padding
        + np.array([0.0, 0.0, height])
    )

    # apply
    cam.position = new_pos.tolist()
    cam.focal_point = target_pos.tolist()
    cam.up = (0, 0, 1)