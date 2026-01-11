from pathlib import Path
from motion.constants import (
    TRAJECTORY,
    ARROW_SCALE,
    SPHERE_RADIUS,
)
from motion.animation_setup import AnimationSetup
from motion.animation_loop import AnimationLoop


def main():
    global_config = {
        "sphere_radius": SPHERE_RADIUS,
        "arrow_scale": ARROW_SCALE,
    }

    project_root = Path(__file__).parent.parent
    config_path = project_root / "data" / "actors_config_flexible.json"

    setup = AnimationSetup(
        TRAJECTORY,
        global_config,
        str(config_path),
        use_kinematics=False
    )

    visualizer, animator, animation_config = setup.setup()
    current_t = setup.get_current_t_dict()

    visualizer.show()

    loop = AnimationLoop(visualizer, current_t)
    loop.run()


if __name__ == "__main__":
    main()