import numpy as np

class deBoor:
	def __init__(self, points, power):
		self.points = points
		self.power = power

		l = len(self.points) + self.power

		self.knots = [1 / l * i for i in range(l + 1)]
		for i in range(power + 1):
			self.knots[i] = 0
			self.knots[-i - 1] = 1

	def get_index(self, t):
		for i in range(self.power, len(self.knots) - self.power - 1):
			if self.knots[i] <= t <= self.knots[i + 1]:
				return i

	def get_point(self, t):
		ind = self.get_index(t)
	
		points = self.points[ind - self.power : ind + 1]
        
		for p in range(self.power):
			cur_points = []
			for i in range(self.power - p):
				st = self.knots[ind - self.power + p + 1 + i]
				fn = self.knots[ind + 1 + i]

				alpha = (t - st) / (fn - st)

				(ux, uy, uw) = points[i]
				(vx, vy, vw) = points[i + 1]
				
				new_x = (1 - alpha) * ux * uw + alpha * vx * vw
				new_y = (1 - alpha) * uy * uw + alpha * vy * vw
				new_weight = (1 - alpha) * uw + alpha * vw

				cur_points.append((new_x / new_weight, new_y / new_weight, new_weight))
			points = cur_points
		
		return points[0]
		

	def get_curve(self, num_points = 100):
		curve = [self.get_point(float(i) / num_points) for i in range(num_points + 1)] 

		return curve