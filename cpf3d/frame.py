from typing import List, Tuple, Union

import numpy as np


class Frame:
	def __init__(self, positions: Union[np.ndarray, List[Tuple[float, float, float]]]):
		self.positions = np.array(positions)

	def __str__(self):
		return f'Frame(#positions={len(self.positions)})'

	def __repr__(self):
		with np.printoptions(threshold=np.inf):
			return f'Frame(positions={self.positions})'