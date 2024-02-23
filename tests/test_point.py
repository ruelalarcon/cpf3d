import pytest

from cpf3d import Point


def test_point_initialization():
	color = (255, 0, 0)
	point = Point(*color)
	assert point.color == color

def test_point_str_representation():
	point = Point(255, 0, 0)
	assert str(point) == 'Point(color=(255, 0, 0))'
