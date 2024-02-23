import numpy as np
import pytest

from cpf3d import Frame, Point, PointFrames


def test_point_frames_initialization():
	pf = PointFrames()
	assert len(pf.points) == 0
	assert len(pf.frames) == 0

def test_add_point():
	pf = PointFrames()
	point = Point(255, 0, 0)
	pf.add_point(point)
	assert pf.points[0] == point

def test_add_point_invalid_positions():
	pf = PointFrames()
	point = Point(255, 0, 0)
	pf.add_point(point)
	pf.add_frame(Frame([[0.0, 0.0, 0.0]]))
	pf.add_frame(Frame([[0.0, 0.0, 1.0]]))

	positions = [(0.0, 1.0, 0.0)]  # Only one position, but two frames exist
	with pytest.raises(ValueError):
		pf.add_point(point, positions)

def test_add_frame():
	pf = PointFrames()
	point = Point(255, 0, 0)
	pf.add_point(point)
	positions = [[1.0, 2.0, 3.0]]
	frame = Frame(positions)
	pf.add_frame(frame)
	assert pf.frames[0] == frame
	assert np.array_equal(pf.frames[0].positions[0], positions[0])

def test_add_frame_before_points():
	pf = PointFrames()
	frame = Frame([[0.0, 0.0, 0.0]])
	with pytest.raises(ValueError):
		pf.add_frame(frame)  # No points exist yet

def test_add_frame_invalid_positions():
	pf = PointFrames()
	point = Point(255, 0, 0)
	positions = [[1.0, 2.0, 3.0]]
	pf.add_point(point, positions)
	frame = Frame([[4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])  # Too many positions
	with pytest.raises(ValueError):
		pf.add_frame(frame)

def test_get_position():
	pf = PointFrames()
	point = Point(255, 0, 0)
	positions = [(1.0, 2.0, 3.0)]
	pf.add_point(point, positions)
	frame = Frame([[1.0, 2.0, 3.0]])
	pf.add_frame(frame)
	assert np.array_equal(pf.get_position(0, 0), np.array([1.0, 2.0, 3.0]))

def test_get_positions():
	pf = PointFrames()
	point = Point(255, 0, 0)
	positions = [(1.0, 2.0, 3.0)]
	pf.add_point(point, positions)
	frame = Frame([[1.0, 2.0, 3.0]])
	pf.add_frame(frame)
	assert np.array_equal(pf.get_positions(0), np.array([[1.0, 2.0, 3.0]]))

def test_apply_offset():
	pf = PointFrames()
	point = Point(255, 0, 0)
	positions = [(1.0, 2.0, 3.0)]
	pf.add_point(point, positions)
	frame = Frame([[1.0, 2.0, 3.0]])
	pf.add_frame(frame)
	pf.apply_offset(1.0, 1.0, 1.0)
	assert np.array_equal(pf.get_position(0, 0), np.array([2.0, 3.0, 4.0]))

def test_apply_rotation():
	pf = PointFrames()
	point = Point(255, 0, 0)
	positions = [(1.0, 0.0, 0.0)]
	pf.add_point(point, positions)
	frame = Frame([[1.0, 0.0, 0.0]])
	pf.add_frame(frame)
	pf.apply_rotation(0.0, 90.0, 0.0)  # Rotate 90 degrees around the Y-axis
	np.testing.assert_almost_equal(pf.get_position(0, 0), np.array([0.0, 0.0, -1.0]), decimal=5)

def test_apply_scale():
	pf = PointFrames()
	point = Point(255, 0, 0)
	positions = [(1.0, 2.0, 3.0)]
	pf.add_point(point, positions)
	frame = Frame([[1.0, 2.0, 3.0]])
	pf.add_frame(frame)
	pf.apply_scale(2.0, 2.0, 2.0)
	assert np.array_equal(pf.get_position(0, 0), np.array([2.0, 4.0, 6.0]))

def test_point_frames_str_representation():
	pf = PointFrames()
	point = Point(255, 0, 0)
	pf.add_point(point)
	frame = Frame(np.array([[1.0, 2.0, 3.0]]))
	pf.add_frame(frame)
	assert str(pf) == 'PointFrames(#points=1, #frames=1)'

def test_point_frames_repr_representation():
	pf = PointFrames()
	point = Point(255, 0, 0)
	pf.add_point(point)
	frame = Frame(np.array([[1.0, 2.0, 3.0]]))
	pf.add_frame(frame)
	assert repr(pf) == 'PointFrames(points=[Point(color=(255, 0, 0))], frames=[Frame(positions=[[1. 2. 3.]])])'
