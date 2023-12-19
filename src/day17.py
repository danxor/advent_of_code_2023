#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
import heapq

class Day17(DaySolve, TestSolve):
	def __init__(self):
		self.grid = None
		self.w = None
		self.h = None
		self.test_data = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

	def parse(self, data: str):
		self.grid = [ list(map(int, line)) for line in data.splitlines() ]
		self.h = len(self.grid)
		self.w = len(self.grid[0])

	def neighbors(self, x: int, y: int, px: int, py: int, start: int, stop: int) -> list:
		result = []

		if x == px:
			for i in range(start, stop):
				if 0 <= x + i < self.w:
					n = (x + i, y), sum(self.grid[y][x + k] for k in range(1, i + 1))
					result.append(n)

			for i in range(-start, -stop, -1):
				if 0 <= x + i < self.w:
					n = (x + i, y), sum(self.grid[y][x + k] for k in range(-1, i - 1, -1))
					result.append(n)

		if y == py:
			for i in range(start, stop):
				if 0 <= y + i < self.h:
					n = (x, y + i), sum(self.grid[y + k][x] for k in range(1, i + 1))
					result.append(n)

			for i in range(-start, -stop, -1):
				if 0 <= y + i < self.h:
					n = (x, y + i), sum(self.grid[y + k][x] for k in range(-1, i - 1, -1))
					result.append(n)

		return result
	
	def walk(self, start: int, stop: int) -> int:
		v = set()
		q = [(0, 0, 0, 0, 0)]

		while q:
			h, x, y, px, py = heapq.heappop(q)
			state = (x, y, px, py)
			if state not in v:
				v.add(state)

				if (x, y) == (self.w - 1, self.h - 1):
					return h
				
				for neighbor in self.neighbors(x, y, px, py, start, stop):
					pos, cost = neighbor
					heapq.heappush(q, (h + cost, pos[0], pos[1], x, y))

		return None

	def part1(self) -> str:
		return str(self.walk(1, 4))

	def part2(self) -> str:
		return str(self.walk(4, 11))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '102')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '94')

if __name__ == '__main__':
	with open('../data/input17.txt', 'r') as f:
		data = f.read()

	solver = Day17()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
