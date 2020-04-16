from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QKeySequence
from curve import Curve

def distance(x1, y1, x2, y2):
	return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class Board(QtWidgets.QFrame):
	def __init__(self, parent):
		super().__init__(parent)

		self.setGeometry(QtCore.QRect(5, 5, 605, 605))
		self.setMouseTracking(True)
		self.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.setFrameShadow(QtWidgets.QFrame.Raised)
		self.setObjectName("board")
		self.setStyleSheet("QWidget { background-color: %s }" % QtGui.QColor(255, 255, 255).name())

		self.parent = parent

		self.curves = [Curve()]
		self.cur_curve_index = 0

		self.point_dragged = None
		self.point_selected = None
		self.selected_x = None
		self.selected_y = None

	def mousePressEvent(self, event):
		ex = event.x()
		ey = event.y()
		cur_curve = self.curves[self.cur_curve_index]

		for (i, (x, y, w)) in enumerate(cur_curve.points):
			if distance(x, y, ex, ey) < 8:
				self.point_selected = None
				self.point_dragged = i
				self.selected_x = ex
				self.selected_y = ey

		if self.point_dragged is None:
			self.curves[self.cur_curve_index].add_point(ex, ey)

		self.update()

	def mouseMoveEvent(self, event):
		ex = event.x()
		ey = event.y()
		
		if self.point_dragged is not None:
			d = distance(self.selected_x, self.selected_y, ex, ey)
			if d > 8:
				self.pointSelected = None
				i = self.point_dragged
				
				self.curves[self.cur_curve_index].move_point(i, ex, ey)
				
				self.update()


	def mouseReleaseEvent(self, event):
		ex = event.x()
		ey = event.y()
		if self.point_selected:
			if distance(self.selected_x, self.selected_y, ex, ey) < 8:
				self.point_dragged = None
		if self.point_dragged is not None:
			self.point_selected = self.point_dragged
		self.point_dragged = None
		
		cur_curve = self.curves[self.cur_curve_index]

		for (i, (x, y, w)) in enumerate(cur_curve.points):
			if distance(x, y, ex, ey) < 8:
				self.point_selected = i
				self.selected_x = ex
				self.selected_y = ey

		if self.point_selected is not None:
			x, y, w = cur_curve.points[self.point_selected]
			self.parent.spinBox2.setValue(w)

		self.update()

	def delete_last_point(self):
		cur_curve = self.curves[self.cur_curve_index]
		cur_curve.delete_point()
		if len(cur_curve.points) > 0:
			self.point_selected = len(cur_curve.points) - 1
			(x, y, w) = cur_curve.points[-1]
			self.parent.spinBox2.setValue(w)
		else:
			self.point_selected = None
			
		self.update()

	def delete_curve(self):
		self.curves.pop(self.cur_curve_index)
		if len(self.curves) == 0:
			self.curves.append(Curve())
		self.cur_curve_index = len(self.curves) - 1

		self.update()

	def add_curve(self):
		self.curves.append(Curve())
		self.cur_curve_index = len(self.curves) - 1

		self.update()

	def change_curve(self, index):
		if index < len(self.curves):
			self.cur_curve_index = index

		self.update()

	def set_power(self, power):
		self.curves[self.cur_curve_index].set_power(power)

		self.update()

	def set_weight(self, weight):
		if self.point_selected is not None:
			self.curves[self.cur_curve_index].set_weight(self.point_selected, weight)
			self.update()

	def paintEvent(self, event):
		painter = QPainter(self)

		for (i, curve) in enumerate(self.curves):
			if self.cur_curve_index == i:
				continue
			painter.setPen(QPen(QColor(0, 0, 0)))
			painter.drawPolyline(curve.plot)

		cur_curve = self.curves[self.cur_curve_index]

		painter.setPen(QPen(QColor(0, 0, 0)))
		painter.drawPolyline(cur_curve.get_plot())

		painter.setPen(QPen(QColor(0, 0, 0)))
		painter.setBrush(QBrush(QColor(0, 150, 0)))
		for (i, (x, y, w)) in enumerate(cur_curve.points):
			painter.drawEllipse(x - 2, y - 2, 4, 4)
			painter.drawText(x + 5, y, str(i))
