#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

def parse(line: str) -> list:
	return [ int(x) for x in line.split(' ') ]

def apply_delta(numbers: list, f) -> int:
	delta = [ b - a for a, b in zip(numbers, numbers[1:]) ]
	if all([ x == 0 for x in delta ]): return 0
	val = apply_delta(delta, f)
	return f(delta, val)

class Day9(DaySolve, TestSolve):
	def __init__(self):
		self.numbers = None
		self.test_data = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''

	def parse(self, data: str):
		self.numbers = [ parse(line) for line in data.splitlines() ]

	def part1(self) -> str:
		return str(sum( num[-1] + apply_delta(num, lambda l, x: l[-1] + x) for num in self.numbers ))

	def part2(self) -> str:
		return str(sum( num[0]  - apply_delta(num, lambda l, x: l[0]  - x) for num in self.numbers ))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '114')

	def test2(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '2')

if __name__ == '__main__':
	with open('../data/input9.txt', 'r') as f:
		data = f.read()

	solver = Day9()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
