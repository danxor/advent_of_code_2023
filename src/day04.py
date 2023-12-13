#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass

@dataclass
class Card:
	id: int
	win: set
	hand: set

	def matches(self) -> int:
		return len(self.win.intersection(self.hand))

	def points(self) -> int:
		n = self.matches()
		if n > 0: return 2**(n - 1)
		return 0

	@staticmethod
	def parse(line: str):
		x = line.split(': ')
		w, h = x[1].split(' | ')
		return Card(int(x[0][5:]), { int(n) for n in w.split() }, { int(n) for n in h.split() })

class Day4(DaySolve, TestSolve):
	def __init__(self):
		self.cards = None
		self.test_data = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

	def parse(self, data: str):
		self.cards = {}
		for line in data.splitlines():
			c = Card.parse(line)
			self.cards[c.id] = c

	def part1(self) -> str:
		return str(sum(card.points() for card in self.cards.values()))

	def part2(self) -> str:
		num_cards = {}

		for c in self.cards.values():
			num_cards[c.id] = 1

		for card in self.cards.values():
			for idx in range(card.matches()):
				num_cards[card.id + idx + 1] += num_cards[card.id]

		return str(sum(num_cards.values()))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '13')

	def test2(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '30')

	def clear(self):
		self.parsed = False

if __name__ == '__main__':
	with open('../data/input4.txt', 'r') as f:
		data = f.read()

	solver = Day4()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
