import time
from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
    STEPS,
    FRAME_DELAY,
)
from motion.animation_math import TrajectoryAnimator
from motion.visualization import TrajectoryVisualizer, ActorConfig


def main():
    # Инициализация
    animator = TrajectoryAnimator(TRAJECTORY)

    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config)

    # ========================================
    # КОНФИГУРАЦИЯ ОБЪЕКТОВ (определяется снаружи!)
    # ========================================

    # Метод 1: интерполяция по параметру
    method_1_actors = [
        ActorConfig(
            name="sphere",
            color="red",
            mesh_type="sphere",
            mesh_params={"radius": SPHERE_RADIUS}
        ),
        ActorConfig(
            name="arrow",
            color="red",
            mesh_type="arrow",
            mesh_params={"direction": (1, 0, 0), "scale": ARROW_SCALE}
        ),
    ]
    visualizer.add_actor_group("method_1", method_1_actors)

    # Метод 2: интерполяция по длине дуги
    method_2_actors = [
        ActorConfig(
            name="sphere",
            color="cyan",
            mesh_type="sphere",
            mesh_params={"radius": SPHERE_RADIUS}
        ),
        ActorConfig(
            name="arrow",
            color="cyan",
            mesh_type="arrow",
            mesh_params={"direction": (1, 0, 0), "scale": ARROW_SCALE}
        ),
    ]
    visualizer.add_actor_group("method_2", method_2_actors)

    # ========================================

    visualizer.show()

    # Главный цикл анимации
    try:
        while True:
            for i in range(STEPS):
                t = i / (STEPS - 1)

                # Получить математическое состояние
                state_1 = animator.get_state_by_parameter(t)
                state_2 = animator.get_state_by_length(t)

                # Отрисовать оба метода
                visualizer.update_actor_state("method_1", "sphere", state_1)
                visualizer.update_actor_state("method_1", "arrow", state_1)

                visualizer.update_actor_state("method_2", "sphere", state_2)
                visualizer.update_actor_state("method_2", "arrow", state_2)

                visualizer.update()
                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()