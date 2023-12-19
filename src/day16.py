#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from collections import deque

class Day16(DaySolve, TestSolve):
	def __init__(self):
		self.grid = None
		self.w = None
		self.h = None
		self.test_data = '''.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''

	def parse(self, data: str):
		self.grid = [ line for line in data.splitlines() ]
		self.h = len(self.grid)
		self.w = len(self.grid[0])

	def energized(self, x: int, y: int, d: str) -> int:
		v = set()
		q = deque([(x, y, d)])

		while q:
			x, y, d = q.pop()
			if 0 <= y < self.h and 0 <= x < self.w and (x, y, d) not in v:
				v.add((x, y, d))

				match self.grid[y][x], d:
					case ('.', 'right') | ('/', 'up') | ('\\', 'down') | ('-', 'right'):
						q.append((x + 1, y, 'right'))
					case ('.', 'left') | ('/', 'down') | ('\\', 'up') | ('-', 'left'):
						q.append((x - 1, y, 'left'))
					case ('.', 'down') | ('/', 'left') | ('\\', 'right') | ('|', 'down'):
						q.append((x, y + 1, 'down'))
					case ('.', 'up') | ('/', 'right') | ('\\', 'left') | ('|', 'up'):
						q.append((x, y - 1, 'up'))
					case ('|', 'right') | ('|', 'left'):
						q.append((x, y + 1, 'down'))
						q.append((x, y - 1, 'up'))
					case ('-', 'down') | ('-', 'up'):
						q.append((x + 1, y, 'right'))
						q.append((x - 1, y, 'left'))

		return len(set((r, c) for (r, c, _) in v))

	def part1(self) -> str:
		return str(self.energized(0, 0, 'right'))

	def part2(self) -> str:
		m = 0

		for y in range(self.h):
			z = self.energized(0, y, 'right')
			if z > m: m = z
			z = self.energized(self.w - 1, y, 'left')
			if z > m: m = z

		for x in range(self.w):
			z = self.energized(x, 0, 'down')
			if z > m: m = z
			z = self.energized(x, self.h - 1, 'up')
			if z > m: m = z

		return str(m)

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '46')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '51')

if __name__ == '__main__':
	with open('../data/input16.txt', 'r') as f:
		data = f.read()

	solver = Day16()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
