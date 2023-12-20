#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass
from collections import deque
from typing import Protocol
import math

class Gate(Protocol):
	name: str
	output: list[str]

	def receive(self, sender: str, pulse: int, queue: deque):
		pass

@dataclass	
class FlipFlop(Gate):
	def __init__(self, name, default_value: int, output):
		self.name = name
		self.value = default_value
		self.output = output

	def receive(self, sender: str, pulse: int, queue: deque):
		if pulse == 0:
			self.value = 1 if self.value == 0 else 0
			for gate in self.output:
				queue.append((gate, self.name, self.value))

	def __repr__(self):
		return f'FlipFlop[{self.name}]: {self.output}'

@dataclass	
class Conjunction(Gate):
	input: dict[str, int]

	def __init__(self, name, input, output):
		self.name = name
		self.input = input
		self.output = output

	def receive(self, sender: str, pulse: int, queue: deque):
		self.input[sender] = pulse

		if 0 in self.input.values():
			for gate in self.output:
				queue.append((gate, self.name, 1))
		else:
			for gate in self.output:
				queue.append((gate, self.name, 0))

	def __repr__(self):
		return f'Conjunction[{self.name}]: {self.output}'

@dataclass	
class Broadcaster(Gate):
	def __init__(self, name, output):
		self.name = name
		self.output = output

	def receive(self, sender: str, pulse: int, queue: deque):
		for gate in self.output:
			queue.append((gate, self.name, 0))

	def __repr__(self):
		return f'Broadcaster[{self.name}]: {self.output}'

@dataclass	
class Endpoint(Gate):
	def __init__(self, name: str):
		self.name = name
		self.output = []

	def receive(self, sender: str, pulse: int, queue: deque):
		return

	def __repr__(self):
		return f'Endpoint[{self.name}]'
	
class Day20(DaySolve, TestSolve):
	def __init__(self):
		self.gates = None
		self.test_data = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

	def parse(self, data: str):
		self.gates = {}
		for line in data.splitlines():
			name, _, *output = line.split()
			output = [ x.strip(',') for x in output ]
			if name[0] == '%':
				self.gates[name[1:]] = FlipFlop(name[1:], 0, output)
			elif name[0] == '&':
				self.gates[name[1:]] = Conjunction(name[1:], {}, output)
			elif name == 'broadcaster':
				self.gates[name] = Broadcaster(name, output)
			else:
				self.gates[name] = Endpoint(name)

		for target in [ name for gate in self.gates.values() for name in gate.output ]:
			if target not in self.gates:
				self.gates[target] = Endpoint(target)

		for gate in self.gates.values():
			for target in gate.output:
				g = self.gates[target]
				if isinstance(g, Conjunction):
					g.input[gate.name] = 0

	def part1(self) -> str:
		high, low = 0, 0
		
		queue = deque()
		for _ in range(1000):
			queue.append(('broadcaster', 'button', 0))
			while queue:
				target, sender, pulse = queue.popleft()

				if pulse == 0:
					low += 1
				else:
					high += 1

				g = self.gates[target].receive(sender, pulse, queue)

		return str(high * low)

	def part2(self) -> str:
		if 'rx' not in self.gates:
			return 'undefined'

		found = None

		for gate in self.gates.values():
			if 'rx' in gate.output:
				found = gate
				break

		if found == None:
			return 'rx has no parent'

		tracker = dict([ (name, []) for name in self.gates[found.name].input.keys()])

		queue = deque()
		for n in range(1000000000000000000000000000):
			queue.append(('broadcaster', 'button', 0))
			while queue:
				target, sender, pulse = queue.popleft()
				if target == found.name and pulse == 1:
					if not len(tracker[sender]) > 3:
						tracker[sender].append(n + 1)

					if all([ len(x) > 3 for x in tracker.values() ]):
						return math.lcm(*[ x[-1] - x[-2] for x in tracker.values() ])

				g = self.gates[target].receive(sender, pulse, queue)

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '32000000')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == 'undefined')

if __name__ == '__main__':
	with open('../data/input20.txt', 'r') as f:
		data = f.read()

	solver = Day20()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
