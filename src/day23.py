#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from collections import defaultdict, deque
from copy import deepcopy

class Day23(DaySolve, TestSolve):
	def __init__(self):
		self.map = None
		self.width = None
		self.height = None
		self.start = None
		self.end = None
		self.test_data = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''

	def parse(self, data: str):
		self.map = dict()
		for y, line in enumerate(data.splitlines()):
			self.height = y + 1
			for x, ch in enumerate(line):
				self.map[(x, y)] = ch
				self.width = x + 1

		self.start = (1, 0)
		self.end = (self.width - 2, self.height - 1)

		splits = set()
		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				if self.map[(x, y)] == '.' and sum(self.map[(x + dx, y + dy)] == '#' for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]) < 2:
					splits.add((x, y))

		splits.add((1, 0))
		splits.add((self.width - 2, self.height - 1))

		directions = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}
		queue = deque([(0, (1, 0), (1, 0))])
		explored = set()
		self.edges = defaultdict(set)
		self.reverse = defaultdict(set)

		while queue:
			steps, pos, prev = queue.pop()
			if pos != prev and pos in splits:
				queue.append((0, pos, pos))
				self.edges[prev].add((pos, steps))
				self.reverse[pos].add((prev, steps))
			else:
				for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
					n = (pos[0] + dx, pos[1] + dy)
					if n not in self.map or self.map[n] == '#':
						continue

					ch = self.map[n]
					if ch in directions and (dx, dy) != directions[ch]:
						continue

					if n in splits or n not in explored:
						explored.add(n)
						queue.append((steps + 1, n, prev))


	def walk(self, start: tuple[int, int], end: tuple[int, int], reverse: bool) -> int:
		max_steps = 0
		queue = deque([(0, start, {start})])
		while queue:
			steps, pos, path = queue.pop()
			if pos == end:
				max_steps = max(steps, max_steps)
				continue

			neighbors = self.edges[pos]
			if reverse:
				neighbors = neighbors.union(self.reverse[pos])

			for neighbor, distance in neighbors:
				if neighbor in path:
					continue

				queue.append((steps + distance, neighbor, path.union({neighbor})))

		return max_steps


	def part1(self) -> str:
		return str(self.walk(self.start, self.end, False))

	def part2(self) -> str:
		return str(self.walk(self.start, self.end, True))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '94')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '154')

if __name__ == '__main__':
	with open('../data/input23.txt', 'r') as f:
		data = f.read()

	solver = Day23()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
