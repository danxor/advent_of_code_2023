#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from itertools import combinations

def dist(x1: int, y1: int, x2: int, y2: int, rows: list[int], cols: list[int], factor: int) -> int:
	return abs((x1 + cols[x1] * factor) - (x2 + cols[x2] * factor)) + abs((y1 + rows[y1] * factor) - (y2 + rows[y2] * factor))

class Day11(DaySolve, TestSolve):
	def __init__(self):
		self.rows = None
		self.cols = None
		self.combination = None
		self.test_data = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

	def parse(self, data: str):
		lines = data.splitlines()

		universe = []
		self.rows = [1] * len(lines)
		self.cols = [1] * len(lines[0])

		for y, line in enumerate(lines):
			for x, ch in enumerate(line):
				if ch == '#':
					universe.append((x, y))
					self.rows[y] = 0
					self.cols[x] = 0

		row = 0
		for i, r in enumerate(self.rows):
			row += r
			self.rows[i] = row

		col = 0
		for i, c in enumerate(self.cols):
			col += c
			self.cols[i] = col
		
		self.combinations = list(combinations(universe, 2))

	def part1(self) -> str:
		return str(sum(dist(u[0], u[1], v[0], v[1], self.rows, self.cols, 2 - 1) for u, v in self.combinations))

	def part2(self, factor = 1_000_000) -> str:
		return str(sum(dist(u[0], u[1], v[0], v[1], self.rows, self.cols, factor - 1) for u, v in self.combinations))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '374')
	
	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2(factor=100)
		return (result, result == '8410')

if __name__ == '__main__':
	with open('../data/input11.txt', 'r') as f:
		data = f.read()

	solver = Day11()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
