import time
from motion.visualization import TrajectoryVisualizer
from motion.constants import STEPS, FRAME_DELAY


class AnimationLoop:
    """Главный цикл анимации"""

    def __init__(self, visualizer: TrajectoryVisualizer,
                 current_t: dict,
                 steps: int = STEPS,
                 frame_delay: float = FRAME_DELAY):
        """
        Args:
            visualizer: визуализатор сцены
            current_t: словарь с текущим временем {"value": 0.0}
            steps: количество шагов в одной итерации
            frame_delay: задержка между кадрами (сек)
        """
        self.visualizer = visualizer
        self.current_t = current_t
        self.steps = steps
        self.frame_delay = frame_delay

    def run(self):
        """Запустить цикл анимации"""
        try:
            while True:
                for i in range(self.steps):
                    self.current_t["value"] = i / (self.steps - 1)
                    self.visualizer.update_all_actors()
                    self.visualizer.update()
                    time.sleep(self.frame_delay)
        except KeyboardInterrupt:
            print("Animation stopped")