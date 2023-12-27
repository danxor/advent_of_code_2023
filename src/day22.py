#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

def project(cube: list[int]) -> list[tuple[int, int]]:
    return [ (x, y) for x in range(cube[0], cube[3] + 1) for y in range(cube[1], cube[4] + 1) ]


class Day22(DaySolve, TestSolve):
	def __init__(self):
		self.cubes = None
		self.supported_by = None
		self.test_data = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''

	def parse(self, data: str):
		cubes = []
		for line in data.splitlines():
			s, e = line.split('~')
			cubes.append([ int(x) for x in s.split(',') ] + [ int(x) for x in e.split(',') ])
		
		self.cubes = sorted(cubes, key=lambda x: x[2])

		has_moved = True
		while has_moved:
			has_moved = False
			for i, cube in enumerate(self.cubes):
				min_z = 1
				z = cube[2]
				projection = project(cube)

				for j, other in enumerate(self.cubes):
					if j == i: continue
					if other[2] >= z or other[5] < min_z: continue

					other_projection = project(other)
					if any((point in other_projection for point in projection)):
						min_z = other[5] + 1

				if min_z < z:
					cube[2] = min_z
					cube[5] -= z - min_z
					has_moved = True

		self.supported_by = [ [] for _ in self.cubes ]
		for i, cube in enumerate(self.cubes):
			projection = project(cube)
			for j, other in enumerate(self.cubes):
				if i == j: continue
				if other[5] + 1 != cube[2]: continue
				other_projection = project(other)
				if any((point in other_projection for point in projection)):
					self.supported_by[i].append(j)

	def part1(self) -> str:
		return str(sum(1 for i in range(len(self.supported_by)) if [i] not in self.supported_by))

	def part2(self) -> str:
		s = 0
		for i in range(len(self.supported_by)):
			removed = [i]
			is_removed = True
			while is_removed:
				is_removed = False
				for j, supports in enumerate(self.supported_by):
					if j in removed or supports == []: continue

					if all((k in removed for k in supports)):
						removed.append(j)
						is_removed = True

			s += len(removed) - 1

		return str(s)

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '5')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '7')

if __name__ == '__main__':
	with open('../data/input22.txt', 'r') as f:
		data = f.read()

	solver = Day22()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
