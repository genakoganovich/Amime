import numpy as np
import matplotlib.pyplot as plt
from motion.trajectory import cumulative_lengths

# Пример траектории
trajectory = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [2, 1, 0]
])

# Вычисляем накопленные длины
cum_lengths = cumulative_lengths(trajectory)

# Визуализация
fig, ax = plt.subplots()
ax.plot(trajectory[:, 0], trajectory[:, 1], 'o-', label='Trajectory')

# Подписываем накопленные длины на каждой точке
for i, length in enumerate(cum_lengths):
    ax.text(trajectory[i, 0], trajectory[i, 1]+0.05, f"{length:.2f}", color='blue', ha='center')

ax.set_aspect('equal')
ax.set_title("Cumulative lengths along trajectory")
ax.legend()
plt.show()
