import struct
from typing import List, Tuple, Union
from zlib import crc32

import numpy as np

from .frame import Frame
from .point import Point


class PointFrames:
	def __init__(self):
		self.points = []
		self.frames = []

	def add_point(self, point: Point, positions: Union[np.ndarray, List[Tuple[float, float, float]]] = None):
		if len(self.frames) != 0 and (positions is None or len(positions) != len(self.frames)):
			raise ValueError('When adding a new point to a PointFrame that already has frames, you must provide a positions array for its position at each frame')
		self.points.append(point)

		if positions is None:
			return

		for frame, position in zip(self.frames, positions):
			frame.positions = np.append(frame.positions, [position], axis=0)

	def add_frame(self, frame: Frame):
		if len(self.points) == 0:
			raise ValueError('Cannot add frames to a PointFrame with no points')

		if len(frame.positions) != len(self.points):
			raise ValueError('Frame must contain 1 position for each existing point')
		self.frames.append(frame)

	def get_position(self, point_index: int, frame_index: int) -> Tuple[float, float, float]:
		return self.frames[frame_index].positions[point_index]

	def get_positions(self, frame_index: int) -> np.ndarray:
		return self.frames[frame_index].positions

	def apply_offset(self, ax1: float, ax2: float, ax3: float):
		offset = (ax1, ax2, ax3)
		for frame in self.frames:
			frame.positions += np.array(offset)

		return self

	def apply_rotation(self, deg1: float, deg2: float, deg3: float):
		degrees = np.radians((deg1, deg2, deg3))

		ax1 = np.array([[1, 0, 0],
					   [0, np.cos(degrees[0]), -np.sin(degrees[0])],
					   [0, np.sin(degrees[0]), np.cos(degrees[0])]])

		ax2 = np.array([[np.cos(degrees[1]), 0, np.sin(degrees[1])],
					   [0, 1, 0],
					   [-np.sin(degrees[1]), 0, np.cos(degrees[1])]])

		ax3 = np.array([[np.cos(degrees[2]), -np.sin(degrees[2]), 0],
					   [np.sin(degrees[2]), np.cos(degrees[2]), 0],
					   [0, 0, 1]])

		rotation_matrix = np.dot(ax3, np.dot(ax2, ax1))

		for frame in self.frames:
			frame.positions = np.dot(frame.positions, rotation_matrix.T)

		return self

	def apply_scale(self, ax1: float, ax2: float, ax3: float):
		scale = (ax1, ax2, ax3)
		for frame in self.frames:
			frame.positions *= np.array(scale)

		return self

	def save(self, file_path: str):
		with open(file_path, 'wb') as file:
			version = 1

			file.write(b'3CPF')
			file.write(struct.pack('I', version))
			checksum_offset = file.tell()
			file.write(b'\x00\x00\x00\x00')
			file.write(struct.pack('I', len(self.points)))
			file.write(struct.pack('I', len(self.frames)))

			point_color_data = bytearray()
			frame_position_data = bytearray()

			for point in self.points:
				point_color_data += struct.pack('3B', *point.color)

			for frame in self.frames:
				for position in frame.positions:
					frame_position_data += struct.pack('3f', *position)

			file.write(point_color_data)
			file.write(frame_position_data)

			checksum = crc32(point_color_data + frame_position_data) & 0xffffffff

		with open(file_path, 'r+b') as file:
			file.seek(checksum_offset)
			file.write(struct.pack('I', checksum))

	def __str__(self):
		return f'PointFrames(#points={len(self.points)}, #frames={len(self.frames)})'

	def __repr__(self):
		return f'PointFrames(points={repr(self.points)}, frames={repr(self.frames)})'

def load(file_path: str, coordinate_order: str = 'xyz') -> PointFrames:
	animation = PointFrames()

	coordinate_order = coordinate_order.lower()
	if len(coordinate_order) != 3 or set(coordinate_order) != {'x', 'y', 'z'}:
		raise ValueError("coordinate_order must be a 3-letter string containing 'x', 'y', and 'z'")

	with open(file_path, 'rb') as file:
		magic_number = file.read(4)
		if magic_number != b'3CPF':
			raise ValueError('Invalid file format')

		version_number, checksum, total_points, total_frames = struct.unpack('4I', file.read(16))

		data_bytes = file.read()
		calculated_checksum = crc32(data_bytes) & 0xffffffff
		if calculated_checksum != checksum:
			raise ValueError('Data corruption detected')

		offset = 0
		for _ in range(total_points):
			r_color, g_color, b_color = struct.unpack_from('3B', data_bytes, offset)
			animation.points.append(Point(r_color, g_color, b_color))
			offset += 3

		indices = [coordinate_order.index('x'), coordinate_order.index('y'), coordinate_order.index('z')]
		for _ in range(total_frames):
			positions = np.empty((total_points, 3), dtype=np.float32)
			for point_index in range(total_points):
				coords = struct.unpack_from('3f', data_bytes, offset)
				positions[point_index] = [coords[i] for i in indices]
				offset += 12
			animation.frames.append(Frame(positions))

	return animation
