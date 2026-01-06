
from motion.kinematics_visualizer import KinematicVisualizer
import numpy as np

points = np.array([
    [0, 0, 0],
    [1, 0.2, 0],
    [2, 1.0, 0],
    [3, 1.2, 0],
    [4, 0.5, 0],
    [5, -0.5, 0],
    [6, -0.8, 0],
])

vis = KinematicVisualizer(points)
vis.run()