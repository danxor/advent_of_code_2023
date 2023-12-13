#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
import functools

@functools.lru_cache(maxsize=None)
def possibilities(conditions: str, nums: tuple) -> int:
	if len(conditions) < sum(nums) + len(nums) - 1:
		return 0

	if '#' in conditions and nums == ():
		return 0

	if len(conditions) == 0:
		return 1

	if nums == ():
		return 1

	c = conditions[0]
	n = nums[0]

	if c == '.':
		return possibilities(conditions[1:], nums)

	if c == '#':
		if '.' in conditions[:n]:
			return 0

		if len(conditions) > n and conditions[n] == '#':
			return 0

		return possibilities(conditions[n + 1:], nums[1:])

	if c == '?':
		left = conditions[1:]
		dot = possibilities('.' + left, nums)
		hash = possibilities('#' + left, nums)
		return dot + hash

def unfold(record: tuple, factor: int) -> tuple:
    conditions, nums = record
    return ('?'.join([conditions] * factor), nums * factor)

class Day12(DaySolve, TestSolve):
	def __init__(self):
		self.records = None
		self.test_data = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''

	def parse(self, data: str):
		self.records = []
		for line in data.splitlines():
			conditions, nums = line.split()
			groups = tuple([int(x) for x in nums.split(',')])
			self.records.append((conditions, groups))

	def part1(self) -> str:
		s = 0
		for record in self.records:
			s += possibilities(*record)
		return str(s)

	def part2(self) -> str:
		s = 0
		for record in self.records:
			new_record = unfold(record, 5)
			s += possibilities(*new_record)
		return str(s)

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '21')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '525152')

if __name__ == '__main__':
	with open('../data/input12.txt', 'r') as f:
		data = f.read()

	solver = Day12()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
