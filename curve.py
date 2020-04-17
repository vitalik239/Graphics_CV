from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF
from nurbs import DeBoor

class Curve:
	def __init__(self, power = 1):
		self.points = []
		self.power = power

		self.is_changed = True
		self.plot = None

	def set_power(self, power):
		self.power = power
		self.is_changed = True

	def add_point(self, x, y, weight = 1):
		self.points.append((x, y, weight))
		self.is_changed = True

	def delete_point(self):
		if len(self.points) > 0:
			del self.points[-1]
		self.is_changed = True

	def move_point(self, index, x, y):
		(xx, yy, w) = self.points[index]
		self.points[index] = (x, y, w)
		self.is_changed = True

	def set_weight(self, index, weight):
		(x, y, w) = self.points[index]
		self.points[index] = (x, y, weight)
		self.is_changed = True

	def draw_plot(self):
		if self.power == 1:
			new_points = self.points
		elif self.power <= len(self.points) - 1:
			new_points = DeBoor(self.points, self.power).get_curve()
		else:
			new_points = []
		self.plot = QPolygonF([QPointF(x, y) for (x, y, w) in new_points])

		self.is_changed = False

	def get_plot(self):
		if self.is_changed:
			self.draw_plot()
		return self.plot
