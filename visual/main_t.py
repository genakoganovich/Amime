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


def main():
    # Простой словарь вместо класса
    current_state = {"t": 0.0}

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

    for actor_name, actor_cfg in actor_config.get_all_actors().items():
        visualizer.add_actor(actor_cfg)


    # ========================================
    # РЕГИСТРАЦИЯ ПРОВАЙДЕРОВ СОСТОЯНИЯ
    # ========================================

    # Используем current_t из локальной области
    visualizer.register_state_provider(
        "method_1_sphere",
        lambda: ActorState(
            position=animator.get_state_by_parameter(current_state["t"])["position"],
            yaw=animator.get_state_by_parameter(current_state["t"])["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_1_arrow",
        lambda: ActorState(
            position=animator.get_state_by_parameter(current_state["t"])["position"],
            yaw=animator.get_state_by_parameter(current_state["t"])["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_2_sphere",
        lambda: ActorState(
            position=animator.get_state_by_length(current_state["t"])["position"],
            yaw=animator.get_state_by_length(current_state["t"])["yaw"]
        )
    )

    visualizer.register_state_provider(
        "method_2_arrow",
        lambda: ActorState(
            position=animator.get_state_by_length(current_state["t"])["position"],
            yaw=animator.get_state_by_length(current_state["t"])["yaw"]
        )
    )

    visualizer.show()

    # ========================================
    # ГЛАВНЫЙ ЦИКЛ АНИМАЦИИ
    # ========================================
    try:
        while True:
            for i in range(STEPS):
                current_state["t"] = i / (STEPS - 1)
                visualizer.update_all_actors()
                visualizer.update()
                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()