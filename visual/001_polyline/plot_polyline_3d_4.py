import numpy as np
import matplotlib.pyplot as plt
from motion.trajectory import polyline_length, cumulative_lengths
import time

# --- Генерируем траекторию ---
t = np.linspace(0, 4 * np.pi, 50)
trajectory = np.column_stack([
    np.cos(t),  # X
    np.sin(t),  # Y
    0.1 * t  # Z
])

# --- Вычисляем длины ---
cum_lengths = cumulative_lengths(trajectory)
segment_lengths = np.diff(cum_lengths)
total_length = polyline_length(trajectory)

# --- Настройка графика ---
plt.ion()  # интерактивный режим
fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)


def init_ax2():
    ax2.set_xlim(0, len(cum_lengths) - 1)
    ax2.set_ylim(0, cum_lengths[-1] + 0.1)
    ax2.set_title("Cumulative Length along Trajectory")
    ax2.set_xlabel("Point index")
    ax2.set_ylabel("Cumulative length")
    ax2.grid(True)


init_ax2()

# --- Бесконечная анимация с окраской пройденных сегментов ---
while True:
    # очищаем линии для новой итерации
    ax1.cla()
    init_ax2()

    # создаём линию для накопленной длины
    line_cum, = ax2.plot([], [], marker='o', color='blue')

    for i in range(1, len(trajectory) + 1):
        # --- 3D траектория ---
        # рисуем все сегменты, которые уже пройдены
        for j in range(i - 1):
            seg = trajectory[j:j + 2]
            # пройденные сегменты красные
            color = 'red' if j < i - 1 else plt.cm.viridis(segment_lengths[j] / segment_lengths.max())
            ax1.plot(seg[:, 0], seg[:, 1], seg[:, 2], color=color, linewidth=3)

        # рисуем текущий шар
        ax1.scatter(*trajectory[i - 1], color='red', s=100, label='Object')
        ax1.set_title("3D Trajectory (segment length color)")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")

        # --- Накопленная длина ---
        line_cum.set_data(np.arange(i), cum_lengths[:i])
        ax2.relim()
        ax2.autoscale_view()

        plt.pause(0.2)  # задержка для анимации

    # пауза в конце траектории
    time.sleep(1.0)
