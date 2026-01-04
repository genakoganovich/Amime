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
cum_lengths = cumulative_lengths(trajectory)
segment_lengths = np.diff(cum_lengths)
total_length = polyline_length(trajectory)

print(f"Total polyline length: {total_length:.2f}")

# --- Визуализация сегментов с цветом, зависящим от длины сегмента ---
fig = plt.figure(figsize=(10,6))

# 3D траектория с цветными сегментами
ax1 = fig.add_subplot(121, projection='3d')
for i in range(len(trajectory)-1):
    seg = trajectory[i:i+2]
    ax1.plot(seg[:,0], seg[:,1], seg[:,2], color=plt.cm.viridis(segment_lengths[i]/segment_lengths.max()), linewidth=3)
ax1.set_title("3D Trajectory (segment length color)")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
ax1.set_zlabel("Z")

# Накопленная длина
ax2 = fig.add_subplot(122)
ax2.plot(np.arange(len(cum_lengths)), cum_lengths, marker='o', color='blue')
ax2.set_title("Cumulative Length along Trajectory")
ax2.set_xlabel("Point index")
ax2.set_ylabel("Cumulative length")
ax2.grid(True)

plt.tight_layout()
plt.show()
