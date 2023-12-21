#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from collections import defaultdict

class Day21(DaySolve, TestSolve):
	def __init__(self):
		self.map = None
		self.start = None
		self.width = None
		self.height = None
		self.step_directons = [ (0, -1), (0, 1), (1, 0), (-1, 0) ]
		self.test_data = '''...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........'''

	def parse(self, data: str):
		lines = list(data.splitlines())

		self.height = len(lines)
		self.width = 0
		self.map = {}

		for y, line in enumerate(lines):
			self.width = max(self.width, len(line))
			for x, ch in enumerate(line):
				pos = (x, y)
				if ch == 'S':
					self.start = pos
					self.map[pos] = '.'
				else:
					self.map[pos] = ch

	def part1(self) -> str:
		visited = defaultdict(set)
		visited[0].add(self.start)

		for step in range(64):
			for x, y in visited[step]:
				for dx, dy in self.step_directons:
					xx = x + dx
					yy = y + dy
					if (xx, yy) in self.map and self.map[(xx, yy)] in '.S':
						visited[step + 1].add((xx, yy))

		last = visited[len(visited) - 1]

		return str(len(last))

	def part2(self) -> str:
		steps = 26501365
		visited = defaultdict(set)
		visited[0].add(self.start)
		mod = steps % self.width
		prev = 0
		deltas = []

		for step in range(steps):
			for x, y in visited[step]:
				for dx, dy in self.step_directons:
					xx, yy = x + dx, y + dy
					mx, my = xx % self.width, yy % self.height
					if (mx, my) in self.map and self.map[(mx, my)] in '.S':
						visited[step + 1].add((xx, yy))

			if step % self.width == mod:
				deltas.append(len(visited[step]))

			if len(deltas) == 3:
				break

		c = deltas[2] - deltas[1]
		b = deltas[1] - deltas[0]
		a = deltas[0]
		n = steps // self.width
		return str(a + b * n + ( n * (n - 1) // 2) * (c - b))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '42')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '394693535848011')

if __name__ == '__main__':
	with open('../data/input21.txt', 'r') as f:
		data = f.read()

	solver = Day21()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
