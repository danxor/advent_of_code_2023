#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from collections import defaultdict

class Day25(DaySolve, TestSolve):
	def __init__(self):
		self.test_data = '''jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr'''

	def parse(self, data: str):
		self.nodes = defaultdict(set)
		for line in data.splitlines():
			name, *others = line.replace(':', '').split(' ')
			for other in others:
				self.nodes[name].add(other)
				self.nodes[other].add(name)

	def part1(self) -> str:
		split = set(self.nodes)

		delta = lambda v: len(self.nodes[v] - split)

		while sum(map(delta, split)) != 3:
			split.remove(max(split, key=delta))

		return str(len(split) * len(set(self.nodes) - split))

	def part2(self) -> str:
		return 'Merry Christmas!'

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '54')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == 'Merry Christmas!')

if __name__ == '__main__':
	with open('../data/input25.txt', 'r') as f:
		data = f.read()

	solver = Day25()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
