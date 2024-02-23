import os

import numpy as np
import pytest

from cpf3d import Frame, Point, PointFrames, load


def test_load_invalid_format():
	with pytest.raises(ValueError):
		load('tests/data/invalid_format.3cpf')

def test_load_corrupted_file():
	with pytest.raises(ValueError):
		load('tests/data/invalid_checksum.3cpf')

def test_load_valid_file():
	pf = load('tests/data/valid.3cpf')  # A one-frame 3cpf with one red point at position 1,2,3
	assert(len(pf.points) == 1)
	assert(len(pf.frames) == 1)
	assert(repr(pf) == 'PointFrames(points=[Point(color=(255, 0, 0))], frames=[Frame(positions=[[1. 2. 3.]])])')

def test_load_large_file():
	pf = load('tests/data/miku_example.3cpf')  # An example of a 3cpf animation of Hatsune Miku (TDA Model + Seto's Tell Your World Motions)
	assert(len(pf.points) == 600)
	assert(len(pf.frames) == 60)
	assert(pf.points[200].color == (22, 83, 145))

def test_save_and_load():
	pf = PointFrames()
	point1 = Point(255, 0, 0)
	point2 = Point(0, 255, 0)
	pf.add_point(point1)
	pf.add_point(point2)
	frame1 = Frame([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0]])
	frame2 = Frame([[4.0, 5.0, 6.0], [4.0, 5.0, 6.0]])
	pf.add_frame(frame1)
	pf.add_frame(frame2)
	save_path = 'tests/data/test.3cpf'
	pf.save(save_path)
	loaded_pf = load(save_path)
	assert loaded_pf.points[0].color == (255, 0, 0)
	assert loaded_pf.points[1].color == (0, 255, 0)
	assert np.array_equal(loaded_pf.get_position(point_index=0, frame_index=0), np.array([1.0, 2.0, 3.0]))
	assert np.array_equal(loaded_pf.get_position(point_index=0, frame_index=1), np.array([4.0, 5.0, 6.0]))
	assert np.array_equal(loaded_pf.get_position(point_index=1, frame_index=0), np.array([1.0, 2.0, 3.0]))
	assert np.array_equal(loaded_pf.get_position(point_index=1, frame_index=1), np.array([4.0, 5.0, 6.0]))
	os.remove(save_path)