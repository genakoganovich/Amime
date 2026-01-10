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
from motion.mesh_factory import MeshFactory
from motion.actor_configuration import (
    DefaultActorConfiguration,
    ActorConfigurationBuilder,
    ActorConfigFactory,
)


def main():
    # Инициализация
    animator = TrajectoryAnimator(TRAJECTORY)

    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }

    # Создаем фабрику для mesh
    mesh_factory = MeshFactory()

    # Создаем визуализатор
    visualizer = TrajectoryVisualizer(TRAJECTORY, global_config, mesh_factory)

    # ========================================
    # КОНФИГУРАЦИЯ ОБЪЕКТОВ
    # ========================================

    # дефолтная конфигурация
    actor_config = DefaultActorConfiguration(global_config)

    # ========================================

    # Добавляем все группы на сцену
    for group_name, group_config in actor_config.get_all_groups().items():
        visualizer.add_actor_group(group_name, group_config.actors)

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
                visualizer.update_actor_state("method_1", "method_1_sphere", state_1)
                visualizer.update_actor_state("method_1", "method_1_arrow", state_1)

                visualizer.update_actor_state("method_2", "method_2_sphere", state_2)
                visualizer.update_actor_state("method_2", "method_2_arrow", state_2)

                visualizer.update()
                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()