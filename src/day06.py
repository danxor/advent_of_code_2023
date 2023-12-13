#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass

@dataclass
class Race:
	time: str
	max_distance: int

	def get_winners(self) -> int:
		win = 0
		over = False
		for hold in range(1, self.time):
			c = hold * (self.time - hold)
			if c > self.max_distance:
				win += 1
				over = True
			elif over:
				break
		return win

class Day6(DaySolve, TestSolve):
	def __init__(self):
		self.time_line = None
		self.distance_line = None
		self.test_data = '''Time:      7  15   30
Distance:  9  40  200'''

	def parse(self, data: str):
		self.time_line, self.distance_line = ( line[9:] for line in data.splitlines() )
		self.parsed = True

	def part1(self) -> str:
		times = [ int(x) for x in self.time_line.split(' ') if len(x) > 0 ]
		distances = [ int(x) for x in self.distance_line.split(' ') if len(x) > 0 ] 

		races = [ Race(time, distance) for time, distance in zip(times, distances) ]

		a = 1

		for race in races:
			a *= race.get_winners()

		return str(a)

	def part2(self) -> str:
		time = int(''.join(c for c in self.time_line if c in '1234567890'))
		distance = int(''.join(c for c in self.distance_line if c in '1234567890'))

		race = Race(time, distance)

		return str(race.get_winners())

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '288')

	def test2(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '71503')

	def clear(self):
		self.parsed = False

if __name__ == '__main__':
	with open('../data/input6.txt', 'r') as f:
		data = f.read()

	solver = Day6()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
