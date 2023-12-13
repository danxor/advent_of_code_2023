#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass
from math import lcm

@dataclass
class Node:
	name: str
	left: str
	right: str

	@staticmethod
	def parse(line: str):
		x = line.split(' = ')

		name = x[0]
		n = x[1].split(',')

		left = ''.join([ c for c in n[0] if c in 'ACBDEFGHIJKLMNNOPQRSTUVWXYZ1234567890' ])
		right = ''.join([ c for c in n[1] if c in 'ACBDEFGHIJKLMNNOPQRSTUVWXYZ1234567890' ])

		return Node(name, left, right)

def walk(nodes: dict, inst: str, start: str, is_end) -> int:
	steps = 0
	cur = start
	
	while not is_end(cur):
		idx = steps % len(inst)
		node = nodes[cur]
		if inst[idx] == 'L': next = node.left
		elif inst[idx] == 'R': next = node.right
		else: raise ValueError(f'Found and invalid direction: {inst[idx]}')
		cur = next
		steps += 1

	return (steps, cur)

class Day8(DaySolve, TestSolve):
	def __init__(self):
		self.inst = None
		self.nodes = None

	def parse(self, data: str):
		lines = data.splitlines()
		self.inst = lines[0]
		self.nodes = {}
		for node in [ Node.parse(line) for line in lines[2:] ]:
			self.nodes[node.name] = node

	def part1(self) -> str:
		count, _ = walk(self.nodes, self.inst, 'AAA', is_end=lambda x: x == 'ZZZ')
		return str(count)

	def part2(self) -> str:
		curs = [ node for node in self.nodes.keys() if node.endswith('A') ]
		steps = []

		for start in curs:
			count, end = walk(self.nodes, self.inst, start, is_end=lambda x: x.endswith('Z'))
			steps.append(count)

		return str(lcm(*steps))

	def test1(self) -> tuple[str, bool]:
		self.parse('''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)''')
		result = self.part1()
		return (result, result == '6')

	def test2(self) -> tuple[str, bool]:
		self.parse('''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)''')
		result = self.part2()
		return (result, result == '6')

if __name__ == '__main__':
	with open('../data/input8.txt', 'r') as f:
		data = f.read()

	solver = Day8()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
