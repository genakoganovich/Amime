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

# --- Вычисляем длины ---
total_length = polyline_length(trajectory)
cum_lengths = cumulative_lengths(trajectory)
segment_lengths = np.diff(cum_lengths)

print(f"Total polyline length: {total_length:.2f}")
print(f"Cumulative lengths: {cum_lengths}")
print(f"Segment lengths: {segment_lengths}")

# --- Визуализация ---
fig, ax = plt.subplots()
ax.plot(trajectory[:, 0], trajectory[:, 1], 'o-', color='black', label='Trajectory')

# Подписи накопленной длины на каждой точке
for i, length in enumerate(cum_lengths):
    ax.text(trajectory[i, 0], trajectory[i, 1]+0.05, f"{length:.2f}", color='blue', ha='center')

# Подписи длины каждого сегмента посередине сегмента
for i in range(len(trajectory)-1):
    mid_x = (trajectory[i, 0] + trajectory[i+1, 0]) / 2
    mid_y = (trajectory[i, 1] + trajectory[i+1, 1]) / 2
    ax.text(mid_x, mid_y-0.05, f"{segment_lengths[i]:.2f}", color='red', ha='center')

ax.set_aspect('equal')
ax.set_title("Polyline: segments and cumulative lengths")
ax.legend()
plt.show()
