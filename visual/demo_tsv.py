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
from motion.actor_loader import ActorLoader


def main():
    current_t = {"value": 0.0}

    animator = TrajectoryAnimator(TRAJECTORY)
    global_config = {"sphere_radius": SPHERE_RADIUS, "arrow_scale": ARROW_SCALE}

    mesh_factory = MeshFactory()
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config, mesh_factory)

    # ========================================
    # ЗАГРУЗКА КОНФИГУРАЦИИ ИЗ ФАЙЛА
    # ========================================

    actor_config, animation_config = ActorLoader.load_from_csv(
        "../data/actors_config.tsv",
        global_config
    )

    # ========================================
    # ДОБАВЛЯЕМ АКТОРОВ НА СЦЕНУ
    # ========================================

    def make_provider(method):
        def provider():
            if method == "parameter":
                state = animator.get_state_by_parameter(current_t["value"])
            else:  # length
                state = animator.get_state_by_length(current_t["value"])

            return ActorState(
                position=list(state["position"]),
                yaw=state["yaw"]
            )

        return provider

    # Добавляем на сцену
    for actor_name, actor in actor_config.get_all_actors().items():
        method = animation_config[actor_name]

        visualizer.add_actor_with_provider(
            actor_name,
            actor.visuals,
            make_provider(method)
        )

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