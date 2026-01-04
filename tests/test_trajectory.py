import numpy as np
from motion.trajectory import polyline_length, cumulative_lengths

def test_polyline_length():
    pts = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
    ])
    assert polyline_length(pts) == 2.0

def test_cumulative_lengths():
    pts = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
    ])
    expected = np.array([0.0, 1.0, 2.0])  # расстояния: 0 до первой, 1 до второй, 2 до третьей
    np.testing.assert_allclose(cumulative_lengths(pts), expected, rtol=1e-12)
