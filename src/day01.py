#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('..')
sys.path.append('.')

from common import DaySolve, TestSolve

def rep(s: str) -> str:
	items = [ ('one','1' ), ('two','2'), ('three','3'), ('four','4'), ('five','5'), ('six','6'), ('seven','7'), ('eight','8'), ('nine','9') ]

	r = ''

	for i in range(len(s)):
		for k, v in items:
			if s[i:].startswith(k):
				r += v
			else:
				r += s[i]

	return r

class Day1(DaySolve, TestSolve):
	def __init__(self):
		self.lines = None

	def parse(self, data: str):
		self.lines = data.splitlines()

	def part1(self) -> str:
		return str(sum([ int(x[0] + x[-1]) for x in [ ''.join([c for c in line if c in '1234567890' ]) for line in self.lines ] ]))

	def part2(self) -> str:
		return str(sum([ int(x[0] + x[-1]) for x in [ ''.join([c for c in rep(line) if c in '1234567890' ]) for line in self.lines ] ]))

	def test1(self) -> tuple[str, bool]:
		self.parse('''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet''')
		result = self.part1()
		return (result, result == '142')

	def test2(self) -> tuple[str, bool]:
		self.parse('''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen''')
		result = self.part2()
		return (result, result == '281')

if __name__ == '__main__':
	with open('../data/input1.txt', 'r') as f:
		data = f.read()

	solver = Day1()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
