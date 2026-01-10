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
    current_t = {"value": 0.0}

    animator = TrajectoryAnimator(TRAJECTORY)
    global_config = {"sphere_radius": SPHERE_RADIUS, "arrow_scale": ARROW_SCALE}

    mesh_factory = MeshFactory()
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config, mesh_factory)

    # Конфигурация...
    actor_config = DefaultActorConfiguration(global_config)
    for actor_name, actor_cfg in actor_config.get_all_actors().items():
        visualizer.add_actor(actor_cfg)

    # ========================================
    # РЕГИСТРАЦИЯ ПРОВАЙДЕРОВ
    # ========================================

    # Вспомогательные функции для избежания проблемы с замыканиями
    def make_provider_method_1():
        """Провайдер для метода 1 (по параметру)"""

        def provider():
            state = animator.get_state_by_parameter(current_t["value"])
            return ActorState(
                position=state["position"],
                yaw=state["yaw"]
            )

        return provider

    def make_provider_method_2():
        """Провайдер для метода 2 (по длине)"""

        def provider():
            state = animator.get_state_by_length(current_t["value"])
            return ActorState(
                position=state["position"],
                yaw=state["yaw"]
            )

        return provider

    # Регистрируем провайдеры
    visualizer.register_state_provider("method_1_sphere", make_provider_method_1())
    visualizer.register_state_provider("method_1_arrow", make_provider_method_1())

    visualizer.register_state_provider("method_2_sphere", make_provider_method_2())
    visualizer.register_state_provider("method_2_arrow", make_provider_method_2())

    visualizer.show()

    # ========================================
    # ГЛАВНЫЙ ЦИКЛ АНИМАЦИИ
    # ========================================
    try:
        while True:
            for i in range(STEPS):
                current_t["value"] = i / (STEPS - 1)
                visualizer.update_all_actors()
                visualizer.update()
                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()