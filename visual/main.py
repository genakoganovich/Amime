import time
from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
    STEPS,
    FRAME_DELAY,
)
from motion.animation_math import TrajectoryAnimator
from motion.visualization import TrajectoryVisualizer, ActorState
from motion.mesh_factory import MeshFactory
from motion.actor_configuration import ActorConfigurationBuilder


def main():
    # Инициализация
    animator = TrajectoryAnimator(TRAJECTORY)

    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }

    mesh_factory = MeshFactory()
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config, mesh_factory)

    # ========================================
    # КОНФИГУРАЦИЯ ОБЪЕКТОВ
    # ========================================
    actor_config = ActorConfigurationBuilder(global_config)

    # Метод 1: только сфера
    actor_config.add_sphere_group(
        group_name="method_1_sphere",
        actor_name="sphere",
        color="red"
    )

    # Метод 1: только стрелка
    actor_config.add_arrow_group(
        group_name="method_1_arrow",
        actor_name="arrow",
        color="red"
    )

    # Метод 2: только сфера
    actor_config.add_sphere_group(
        group_name="method_2_sphere",
        actor_name="sphere",
        color="cyan"
    )

    # Метод 2: только стрелка
    actor_config.add_arrow_group(
        group_name="method_2_arrow",
        actor_name="arrow",
        color="cyan"
    )

    # Добавляем все группы на сцену
    for group_name, group_config in actor_config.get_all_groups().items():
        visualizer.add_actor_group(group_name, group_config.actors)

    # ========================================
    # РЕГИСТРАЦИЯ ПРОВАЙДЕРОВ СОСТОЯНИЯ
    # ========================================

    # Метод 1
    visualizer.register_state_provider(
        "method_1_sphere", "sphere",
        lambda: ActorState(
            position=animator.get_state_by_parameter(_current_t.value)["position"],
            yaw=animator.get_state_by_parameter(_current_t.value)["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_1_arrow", "arrow",
        lambda: ActorState(
            position=animator.get_state_by_parameter(_current_t.value)["position"],
            yaw=animator.get_state_by_parameter(_current_t.value)["yaw"]
        )
    )

    # Метод 2
    visualizer.register_state_provider(
        "method_2_sphere", "sphere",
        lambda: ActorState(
            position=animator.get_state_by_length(_current_t.value)["position"],
            yaw=animator.get_state_by_length(_current_t.value)["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_2_arrow", "arrow",
        lambda: ActorState(
            position=animator.get_state_by_length(_current_t.value)["position"],
            yaw=animator.get_state_by_length(_current_t.value)["yaw"]
        )
    )

    visualizer.show()

    # ========================================
    # ГЛАВНЫЙ ЦИКЛ АНИМАЦИИ
    # ========================================
    try:
        while True:
            for i in range(STEPS):
                _current_t.value = i / (STEPS - 1)

                # Единственный вызов - обновить все акторы
                visualizer.update_all_actors()
                visualizer.update()

                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


class _CurrentT:
    """Хранилище текущего времени для лямбд"""

    def __init__(self):
        self.value = 0.0


_current_t = _CurrentT()

if __name__ == "__main__":
    main()