#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass

@dataclass
class Stage:
	name: str
	ranges: tuple[int, int, int]

	def apply_one(self, value: int) -> int:
		for dest, start, len in self.ranges:
			delta = value - start
			if 0 <= delta < len:
				return dest + delta

		return value

	def apply_range(self, ranges: iter):
		all = []

		for dest, start, len in self.ranges:
			stop = start + len

			new_ranges = []

			while ranges:
				s, e = ranges.pop()

				before = (s,min(e,start))
				inter = (max(s, start), min(stop, e))
				after = (max(stop, s), e)

				if before[1] > before[0]: new_ranges.append(before)
				if inter[1] > inter[0]: all.append((inter[0] - start + dest, inter[1] - start + dest))
				if after[1] > after[0]: new_ranges.append(after)

			ranges = new_ranges

		return all + ranges

	@staticmethod
	def parse(lines: str) -> iter:
		parts = lines.splitlines()

		ranges = []
		for l in parts[1:]:
			dest, start, len = [ int(x) for x in l.split(' ') ]
			ranges.append((dest, start, len))

		return Stage(parts[0], ranges)

class Day5(DaySolve, TestSolve):
	def __init__(self):
		self.seeds = None
		self.stages = None
		self.test_data = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

	def parse(self, data: str):
		parts = data.split('\n\n')
		self.seeds = [ int(x) for x in parts[0][7:].split(' ') ]
		self.stages = [ Stage.parse(part) for part in parts[1:]  ]

	def part1(self) -> str:
		location = []

		for x in self.seeds:
			for stage in self.stages:
				x = stage.apply_one(x)
			location.append(x)

		return str(min(location))

	def part2(self) -> str:
		location = []

		for start, len in zip(self.seeds[::2], self.seeds[1::2]):
			ranges = [(start, start + len)]
			for stage in self.stages:
				ranges = stage.apply_range(ranges)

			location.append(min(start for start, _ in ranges))

		return str(min(location))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '35')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '46')

if __name__ == '__main__':
	with open('../data/input5.txt', 'r') as f:
		data = f.read()

	solver = Day5()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
