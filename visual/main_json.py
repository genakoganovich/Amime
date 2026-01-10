import time
from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
    STEPS,
    FRAME_DELAY,
)
from motion.animation_setup import AnimationSetup


def main():
    # ========================================
    # ИНИЦИАЛИЗАЦИЯ
    # ========================================

    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }

    setup = AnimationSetup(TRAJECTORY, global_config, "actors_config.json")
    visualizer, animator, animation_config = setup.setup()
    current_t = setup.get_current_t_dict()

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