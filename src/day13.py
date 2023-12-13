#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

def transpose(map: list) -> list:
    return [ ''.join(x) for x in zip(*map) ]

def error_count(pattern: list, i: int) -> int:
    a = list(reversed(pattern[:i]))
    b = pattern[i:]

    c = 0
    for ra, rb in zip(a, b):
        for ca, cb in zip(ra, rb):
            if ca != cb:
                c += 1

    return c

def find_reflection(map: list, smudge: int) -> int:
    for i in range(1, len(map)):
        if error_count(map, i) == smudge:
            return i

    return None

def get_score(map: list, smudge: int) -> int:
    h = find_reflection(map, smudge)
    if h: return 100 * h
    v = find_reflection(transpose(map), smudge)
    return v if v else 0

class Day13(DaySolve, TestSolve):
	def __init__(self):
		self.maps = None
		self.test_data = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

	def parse(self, data: str):
		self.maps = [ map.splitlines() for map in data.split('\n\n') ]

	def part1(self) -> str:
		return str(sum(get_score(map, 0) for map in self.maps))

	def part2(self) -> str:
		return str(sum(get_score(map, 1) for map in self.maps))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '405')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '400')

if __name__ == '__main__':
	with open('../data/input13.txt', 'r') as f:
		data = f.read()

	solver = Day13()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
