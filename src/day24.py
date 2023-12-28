#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass
from collections import namedtuple
from itertools import combinations
from z3 import *

Point3D = namedtuple('Point3D', ['x', 'y', 'z'])

@dataclass
class Hailstone:
	position: Point3D
	velocity: Point3D

	def intersect_2d(self, other: "Hailstone") -> tuple[int, int]:
		dx = other.position.x - self.position.x
		dy = other.position.y - self.position.y
		det = other.velocity.x * self.velocity.y - other.velocity.y * self.velocity.x
		if det == 0: return None
		u = (dy * other.velocity.x - dx * other.velocity.y) / det
		v = (dy * self.velocity.x - dx * self.velocity.y) / det
		
		if u < 0 or v < 0: return None

		m0 = self.velocity.y / self.velocity.x
		m1 = other.velocity.y / other.velocity.x
		b0 = self.position.y - m0 * self.position.x
		b1 = other.position.y - m1 * other.position.x

		x = (b1 - b0) / (m0 - m1)
		y = m0 * x + b0

		return (x, y)

	@staticmethod
	def parse(line: str) -> "Hailstone":
		u, v = line.split(' @ ')

		position = Point3D(*tuple([ int(x.strip()) for x in u.split(',') ]))
		velocity = Point3D(*tuple([ int(x.strip()) for x in v.split(',') ]))

		return Hailstone(position, velocity)

class Day24(DaySolve, TestSolve):
	def __init__(self):
		self.hailstones = None
		self.test_data = '''19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3'''

	def parse(self, data: str):
		self.hailstones = [ Hailstone.parse(line) for line in data.splitlines() ]
		

	def part1(self, lower: int = 200000000000000, upper: int = 400000000000000) -> str:
		s = 0
		for a, b in combinations(self.hailstones, 2):
			r = a.intersect_2d(b)
			if r and lower <= r[0] <= upper and lower <= r[1] <= upper:
				s += 1
		
		return str(s)

	def part2(self) -> str:
		solver = Solver()

		x = Real("x")
		y = Real("y")
		z = Real("z")

		vx = Real("vx")
		vy = Real("vy")
		vz = Real("vz")

		for i, hail in enumerate(self.hailstones):
			t = Real(f"t_{i}")

			solver.add(x + vx * t == hail.position.x + hail.velocity.x * t)
			solver.add(y + vy * t == hail.position.y + hail.velocity.y * t)
			solver.add(z + vz * t == hail.position.z + hail.velocity.z * t)

		solver.check()
		return str(solver.model().eval(x + y + z))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1(7, 27)
		return (result, result == '2')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '47')

if __name__ == '__main__':
	with open('../data/input24.txt', 'r') as f:
		data = f.read()

	solver = Day24()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
