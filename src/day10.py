#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

VE = (0, 1)
VW = (0, -1)
VN = (-1, 0)
VS = (1, 0)

pipe_exists = {
	'|': (VN, VS),
	'-': (VE, VW),
	'L': (VN, VE),
	'J': (VN, VW),
	'7': (VS, VW),
	'F': (VS, VE),
	'.': (),
	'S': (VN, VE, VW, VS),
}

def get_elem(lines, x, y):
	if 0 <= x < len(lines) and 0 <= y < len(lines[x]):
		return lines[x][y]
	return '.'

def get_loop(lines: list) -> tuple:
	conn = []
	for l in lines:
		conn.append([ set() for _ in l ])

	start = None
	for x in range(len(lines)):
		for y in range(len(lines[x])):
			if get_elem(lines, x, y) == 'S':
				start = (x, y)

			for dx, dy in pipe_exists[lines[x][y]]:
				if (-dx, -dy) in pipe_exists[get_elem(lines, x + dx, y + dy)]:
					conn[x][y].add((dx, dy))

	loop = [start]
	prev = None
	cur = None
	while cur != start:
		x, y = loop[-1]
		dx, dy = next(filter(lambda x: x != prev, conn[x][y]))
		prev = (-dx, -dy)
		cur = (x + dx, y + dy)
		loop.append(cur)

	return conn, loop, len(lines[0]), len(lines)

class Day10(DaySolve, TestSolve):
	def __init__(self):
		self.conn = None
		self.loop = None
		self.max_x = None
		self.max_y = None

	def parse(self, data: str):
		self.conn, self.loop, self.max_y, self.max_x = get_loop(data.splitlines())

	def part1(self) -> str:
		return str((len(self.loop) - 1) // 2)

	def part2(self) -> str:
		s = 0

		for x in range(self.max_x):
			i = False
			d = 0
			for y in range(self.max_y):
				if i and (x, y) not in self.loop:
					s += 1
				elif (x, y) in self.loop:
					if d == 0:
						if VE in self.conn[x][y]:
							if VN in self.conn[x][y]:
								d = -1
							elif VS in self.conn[x][y]:
								d = 1
						else:
							i = not i
					else:
						if VN in self.conn[x][y]:
							if d == 1: i = not i
							d = 0
						elif VS in self.conn[x][y]:
							if d == -1: i = not i
							d = 0

		return str(s)

	def test1(self) -> tuple[str, bool]:
		self.parse('''..F7.
.FJ|.
SJ.L7
|F--J
LJ...''')
		result = self.part1()
		return (result, result == '8')

	def test2(self) -> tuple[str, bool]:
		self.parse('''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L''')
		result = self.part2()
		return (result, result == '10')

if __name__ == '__main__':
	with open('../data/input10.txt', 'r') as f:
		data = f.read()

	solver = Day10()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
