#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

def is_symbol(ch: str) -> bool:
	return ch not in '0123456789.'

def get_elem(s: str, i: int) -> str:
	if 0 <= i < len(s): return s[i]
	return '.'

def find_number_coordinates(s: str) -> list:
	coords = []

	start = None

	for i in range(len(s)):
		if s[i].isdigit():
			if start is None:
				start = i
		else:
			if start is not None:
				coords.append((start, i))
				start = None

	if start is not None:
		coords.append((start, len(s)))

	return coords

def find_numbers(schematic: list) -> list:
	numbers = []

	for y, line in enumerate(schematic):
		for start, stop in find_number_coordinates(line):
			include = False

			if is_symbol(get_elem(line, start - 1)):
				include = True

			if is_symbol(get_elem(line, stop)):
				include = True

			if y > 0:
				for i in range(start - 1, stop + 1):
					if is_symbol(get_elem(schematic[y - 1], i)):
						include = True

			if y < len(schematic) - 1:
				for i in range(start - 1, stop + 1):
					if is_symbol(get_elem(schematic[y + 1], i)):
						include = True

			if include:
				numbers.append((y, start, stop))

	return numbers
	
def find_gears(schematic: list, numbers: list) -> list:
	gears = []

	for y, line in enumerate(schematic):
		for x, ch in enumerate(line):
			if ch == '*':
				adjacent_numbers = []
				for n in numbers:
					if n[0] in [y - 1, y, y + 1] and n[1] - 1 <= x <= n[2]:
						adjacent_numbers.append(int(schematic[n[0]][n[1]:n[2]]))

				if len(adjacent_numbers) == 2:
					gears.append(adjacent_numbers)

	return gears
	
class Day3(DaySolve, TestSolve):
	def __init__(self):
		self.numbers = None
		self.schematic = None
		self.test_data = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''

	def parse(self, data: str):
		self.schematic = [ line.strip() for line in data.splitlines() ]
		self.numbers = find_numbers(self.schematic)

	def part1(self) -> str:
		return str(sum(int(self.schematic[y][start:stop]) for y, start, stop in self.numbers))

	def part2(self) -> str:
		return str(sum(a * b for a, b in find_gears(self.schematic, self.numbers)))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '4361')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '467835')

if __name__ == '__main__':
	with open('../data/input3.txt', 'r') as f:
		data = f.read()

	solver = Day3()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
