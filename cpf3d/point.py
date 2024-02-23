class Point:
	def __init__(self, r: int, g: int, b: int):
		self.color = (r, g, b)

	def __str__(self):
		return f'Point(color={self.color})'

	def __repr__(self):
		return f'Point(color={self.color})'