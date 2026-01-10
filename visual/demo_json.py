from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
)
from motion.animation_setup import AnimationSetup
from motion.animation_loop import AnimationLoop


def main():
    # Инициализация
    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }

    setup = AnimationSetup(TRAJECTORY, global_config, "../data/actors_config.json")
    visualizer, animator, animation_config = setup.setup()
    current_t = setup.get_current_t_dict()

    visualizer.show()

    # Главный цикл
    loop = AnimationLoop(visualizer, current_t)
    loop.run()


if __name__ == "__main__":
    main()