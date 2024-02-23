import numpy as np
import pytest

from cpf3d import Frame


def test_frame_initialization():
	positions = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
	frame = Frame(positions)
	assert np.array_equal(frame.positions, positions)

def test_frame_str_representation():
	frame = Frame(np.array([[1.0, 2.0, 3.0]]))
	assert str(frame) == 'Frame(#positions=1)'

def test_frame_repr_representation():
	frame = Frame(np.array([[1.0, 2.0, 3.0]]))
	assert repr(frame) == 'Frame(positions=[[1. 2. 3.]])'