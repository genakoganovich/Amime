import numpy as np
import matplotlib.pyplot as plt
from motion.trajectory import polyline_length, cumulative_lengths

# Пример траектории
trajectory = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [2, 1, 0]
])

# Вычисляем длину каждого сегмента
diffs = np.diff(trajectory, axis=0)
seg_lengths = np.linalg.norm(diffs, axis=1)

# Общая длина через polyline_length
total_length = polyline_length(trajectory)

# Визуализация
fig, ax = plt.subplots()
ax.plot(trajectory[:, 0], trajectory[:, 1], 'o-', label='Trajectory')

# Подписываем длину каждого сегмента
for i, length in enumerate(seg_lengths):
    x_mid = (trajectory[i, 0] + trajectory[i+1, 0]) / 2
    y_mid = (trajectory[i, 1] + trajectory[i+1, 1]) / 2
    ax.text(x_mid, y_mid, f"{length:.2f}", color='red')

ax.set_aspect('equal')
ax.set_title(f"Polyline length = {total_length:.2f}")
ax.legend()
plt.show()
