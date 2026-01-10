import time
from dataclasses import dataclass
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

@dataclass
class ActorAnimationConfig:
    """Конфиг актора для анимации"""
    actor_name: str
    method: str  # "parameter" или "length"

def main():
    current_t = {"value": 0.0}

    animator = TrajectoryAnimator(TRAJECTORY)
    global_config = {"sphere_radius": SPHERE_RADIUS, "arrow_scale": ARROW_SCALE}

    mesh_factory = MeshFactory()
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config, mesh_factory)

    # ========================================
    # КОНФИГУРАЦИЯ АКТОРОВ
    # ========================================
    actor_config = DefaultActorConfiguration(global_config)

    # Конфигурация анимации
    animation_configs = {
        "method_1": "parameter",
        "method_2": "length",
    }

    # ========================================
    # Создание провайдеров
    # ========================================
    def make_provider(method):
        def provider():
            if method == "parameter":
                state = animator.get_state_by_parameter(current_t["value"])
            else:
                state = animator.get_state_by_length(current_t["value"])

            return ActorState(
                position=state["position"],
                yaw=state["yaw"]
            )

        return provider

    # ========================================
    # Добавляем акторов со своими провайдерами
    # ========================================
    for actor_name, actor in actor_config.get_all_actors().items():
        method = animation_configs[actor_name]

        visualizer.add_actor_with_provider(
            actor_name,
            actor.visuals,
            make_provider(method)
        )

    visualizer.show()

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