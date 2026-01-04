import numpy as np
import matplotlib.pyplot as plt
from motion.trajectory import polyline_length, cumulative_lengths

# --- Генерируем плавную 3D траекторию ---
t = np.linspace(0, 4 * np.pi, 50)
trajectory = np.column_stack([
    np.cos(t),       # X
    np.sin(t),       # Y
    0.1 * t          # Z
])

# --- Вычисляем длины ---
total_length = polyline_length(trajectory)
cum_lengths = cumulative_lengths(trajectory)
segment_lengths = np.diff(cum_lengths)

print(f"Total polyline length: {total_length:.2f}")
print(f"Cumulative lengths: {cum_lengths}")
print(f"Segment lengths: {segment_lengths}")

# --- Визуализация ---
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], 'o-', color='black', label='Trajectory')

# Синие подписи — накопленная длина
for i, length in enumerate(cum_lengths):
    ax.text(trajectory[i, 0], trajectory[i, 1], trajectory[i, 2]+0.02, f"{length:.2f}", color='blue')

# Красные подписи — длины сегментов посередине сегмента
for i in range(len(trajectory)-1):
    mid = (trajectory[i] + trajectory[i+1]) / 2
    ax.text(mid[0], mid[1], mid[2]-0.02, f"{segment_lengths[i]:.2f}", color='red')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title("3D Trajectory: segments and cumulative lengths")
ax.legend()
plt.show()
