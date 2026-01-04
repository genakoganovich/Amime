import numpy as np

from motion.trajectory import (
    interpolate_position,
    interpolate_position_by_length,
    cumulative_lengths,
    polyline_length
)


def test_interpolate_position_at_nodes():
    trajectory = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0]])

    # индекс 0 → первая точка
    np.testing.assert_array_almost_equal(interpolate_position(trajectory, 0), trajectory[0])

    # индекс 1 → вторая точка
    np.testing.assert_array_almost_equal(interpolate_position(trajectory, 1), trajectory[1])

    # индекс 2 → третья точка
    np.testing.assert_array_almost_equal(interpolate_position(trajectory, 2), trajectory[2])


def test_interpolate_position_between_nodes():
    trajectory = np.array([[0, 0, 0], [1, 0, 0]])

    # середина между точками
    mid = interpolate_position(trajectory, 0.5)
    np.testing.assert_array_almost_equal(mid, [0.5, 0, 0])


def test_interpolate_position_out_of_bounds():
    trajectory = np.array([[0, 0, 0], [1, 1, 0]])

    # меньше нуля → вернёт первую точку
    np.testing.assert_array_almost_equal(interpolate_position(trajectory, -1), trajectory[0])

    # больше максимального индекса → вернёт последнюю точку
    np.testing.assert_array_almost_equal(interpolate_position(trajectory, 10), trajectory[-1])


def test_interpolate_position_by_length_basic():
    trajectory = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0]])
    cum_len = cumulative_lengths(trajectory)
    total_len = polyline_length(trajectory)

    # длина 0 → первая точка
    np.testing.assert_array_almost_equal(interpolate_position_by_length(trajectory, 0), trajectory[0])

    # длина total_len → последняя точка
    np.testing.assert_array_almost_equal(interpolate_position_by_length(trajectory, total_len), trajectory[-1])

    # середина первой линии (длина 0.5)
    mid = interpolate_position_by_length(trajectory, 0.5)
    np.testing.assert_array_almost_equal(mid, [0.5, 0, 0])


def test_interpolate_position_by_length_out_of_bounds():
    trajectory = np.array([[0, 0, 0], [1, 0, 0]])
    total_len = polyline_length(trajectory)

    # длина меньше нуля
    np.testing.assert_array_almost_equal(interpolate_position_by_length(trajectory, -0.5), trajectory[0])

    # длина больше total_len
    np.testing.assert_array_almost_equal(interpolate_position_by_length(trajectory, total_len + 1.0), trajectory[-1])
