import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 2 * np.pi, 200)
trajectory = np.column_stack([
    np.cos(t),
    np.sin(t),
    t * 0.1
])

plt.plot(trajectory[:, 0], trajectory[:, 1])
plt.axis("equal")
plt.title("Test trajectory")
plt.show()
