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
)


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
    # ВАРИАНТ 1: Дефолтная конфигурация
    # ========================================
    # actor_config = DefaultActorConfiguration(global_config)

    # ========================================
    # ВАРИАНТ 2: Кастомная конфигурация - разделенные сфера и стрелка
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

    # ========================================
    # ВАРИАНТ 3: Комбинированный подход
    # ========================================
    # actor_config = ActorConfigurationBuilder(global_config)
    #
    # # Метод 1: сфера + стрелка вместе
    # actor_config.add_sphere_and_arrow_group("method_1", color="red")
    #
    # # Метод 2: только сфера
    # actor_config.add_sphere_group(
    #     group_name="method_2",
    #     actor_name="sphere",
    #     color="cyan"
    # )
    #
    # # Метод 3: кастомные размеры
    # actor_config.add_sphere_group(
    #     group_name="method_3",
    #     actor_name="big_sphere",
    #     color="green",
    #     radius=0.15
    # )

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

                state_1 = animator.get_state_by_parameter(t)
                state_2 = animator.get_state_by_length(t)

                # Вариант 2: разделенные группы
                visualizer.update_actor_state("method_1_sphere", "sphere", state_1)
                visualizer.update_actor_state("method_1_arrow", "arrow", state_1)

                visualizer.update_actor_state("method_2_sphere", "sphere", state_2)
                visualizer.update_actor_state("method_2_arrow", "arrow", state_2)

                visualizer.update()
                time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        print("Animation stopped")


if __name__ == "__main__":
    main()