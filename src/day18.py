#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass

@dataclass
class Instruction:
	direction: str
	distance: int

	@staticmethod
	def parse_one(line: str) -> "Instruction":
		direction, distance, _ = line.split(' ')
		return Instruction(direction, int(distance))

	@staticmethod
	def parse_two(line: str) -> "Instruction":
		directions = { '0': 'R', '1': 'D', '2': 'L', '3': 'U' }
		_, __, color = line.split(' ')
		color = color[2:-1]

		return Instruction(directions[color[5]], int(color[:5], 16))

def area(points: list) -> int:
	n = len(points)
	r = 0

	for i in range(n):
		x1, y1 = points[i]
		x2, y2 = points[( i + 1) % n]
		r += (x1 * y2) - (x2 * y1)

	return abs(r) // 2

def n_boundary_points(points: list) -> int:
	n = len(points)
	r = n

	for i in range(n):
		x1, y1 = points[i]
		x2, y2 = points[(i + 1) % n]
		dx = max(0, abs(x1 - x2) - 1)
		dy = max(0, abs(y1 - y2) - 1)
		r += dx + dy

	return r

def n_inner_points(points: list) -> int:
	return area(points) - n_boundary_points(points) // 2 + 1

def polygon_area(points: list) -> int:
	return n_boundary_points(points) + n_inner_points(points)

def solve(instructions: list) -> int:
	deltas = { 'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0) }

	points = []
	x, y = 0, 0

	for instruction in instructions:
		dx, dy = deltas[instruction.direction]
		x += dx * instruction.distance
		y += dy * instruction.distance
		points.append((x, y))

	return polygon_area(points)

class Day18(DaySolve, TestSolve):
	def __init__(self):
		self.instructions_one = None
		self.instructions_two = None
		self.test_data = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

	def parse(self, data: str):
		self.instructions_one = [ Instruction.parse_one(line) for line in data.splitlines() ]
		self.instructions_two = [ Instruction.parse_two(line) for line in data.splitlines() ]

	def part1(self) -> str:
		return str(solve(self.instructions_one))

	def part2(self) -> str:
		return str(solve(self.instructions_two))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '62')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '952408144115')

if __name__ == '__main__':
	with open('../data/input18.txt', 'r') as f:
		data = f.read()

	solver = Day18()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
