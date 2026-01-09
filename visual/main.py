import time
from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
    STEPS,
    FRAME_DELAY,
)
from motion.animation_math import TrajectoryAnimator
from motion.visualization import TrajectoryVisualizer


def main():
    # Инициализация
    animator = TrajectoryAnimator(TRAJECTORY)

    config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }
    visualizer = TrajectoryVisualizer(TRAJECTORY, config)
    visualizer.show()

    # Главный цикл анимации
    try:
        while True:
            for i in range(STEPS):
                t = i / (STEPS - 1)

                # Получить математическое состояние
                state_seg = animator.get_state_by_parameter(t)
                state_len = animator.get_state_by_length(t)

                # Отрисовать
                visualizer.render_frame(state_seg, state_len)

                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()