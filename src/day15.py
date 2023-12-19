#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

def hash(s: str) -> int:
	cur = 0
	for c in s:
		cur += ord(c)
		cur *= 17
		cur = cur % 256
	return cur

def parse(part: str) -> tuple[str, str, int]:
	idx = part.find('=')
	if idx >= 0:
		return (part[0:idx], '=', int(part[idx + 1:]))
	
	idx = part.find('-')
	if idx >= 0:
		return (part[0:idx], '-', None)

	return None

def get_score(boxes: list) -> int:
	s = 0

	for i, box in enumerate(boxes, start=1):
		for j, val in enumerate(box, start=1):
			s += i * j * val[1]

	return s

class Day15(DaySolve, TestSolve):
	def __init__(self):
		self.parts = None
		self.test_data = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''

	def parse(self, data: str):
		self.parts = []
		for line in data.splitlines():
			for part in line.split(','):
				self.parts.append(part)

	def part1(self) -> str:
		return str(sum(hash(part) for part in self.parts))

	def part2(self) -> str:
		boxes = [ [] for _ in range(256) ]

		for part in self.parts:
			label, op, focal = parse(part)
			box = hash(label)

			if op == '=':
				found = next( (x[0] for x in filter(lambda x: x[1][0] == label, enumerate(boxes[box]))), -1)
				if found >= 0:
					boxes[box][found] = (label, focal)
				else:
					boxes[box].append((label, focal))
			elif op == '-':
				if len(boxes[box]) > 0:
					boxes[box] = list(filter(lambda x: x[0] != label, boxes[box]))

		return str(get_score(boxes))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '1320')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '145')

if __name__ == '__main__':
	with open('../data/input15.txt', 'r') as f:
		data = f.read()

	solver = Day15()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
