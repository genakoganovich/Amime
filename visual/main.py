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
from motion.actor_configuration import DefaultActorConfiguration


class _CurrentT:
    """Хранилище текущего времени"""

    def __init__(self):
        self.value = 0.0


_current_t = _CurrentT()


def main():
    animator = TrajectoryAnimator(TRAJECTORY)

    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }

    mesh_factory = MeshFactory()
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config, mesh_factory)

    # ========================================
    # КОНФИГУРАЦИЯ АКТОРОВ
    # ========================================
    actor_config = DefaultActorConfiguration(global_config)

    # Добавляем каждого актора на сцену
    for actor_name, actor_cfg in actor_config.get_all_actors().items():
        visualizer.add_actor(actor_cfg)

    # ========================================
    # РЕГИСТРАЦИЯ ПРОВАЙДЕРОВ СОСТОЯНИЯ
    # ========================================

    # Метод 1: по параметру
    visualizer.register_state_provider(
        "method_1_sphere",
        lambda: ActorState(
            position=animator.get_state_by_parameter(_current_t.value)["position"],
            yaw=animator.get_state_by_parameter(_current_t.value)["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_1_arrow",
        lambda: ActorState(
            position=animator.get_state_by_parameter(_current_t.value)["position"],
            yaw=animator.get_state_by_parameter(_current_t.value)["yaw"]
        )
    )

    # Метод 2: по длине дуги
    visualizer.register_state_provider(
        "method_2_sphere",
        lambda: ActorState(
            position=animator.get_state_by_length(_current_t.value)["position"],
            yaw=animator.get_state_by_length(_current_t.value)["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_2_arrow",
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
                visualizer.update_all_actors()
                visualizer.update()
                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()