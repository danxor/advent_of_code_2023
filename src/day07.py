#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass
from collections import Counter

@dataclass
class HandBid:
	cards: list
	bid: int

	def get_hand_histogram(self) -> Counter:
		hist = Counter()
		for c in self.cards: hist[c] += 1
		return hist

	def get_score(self, joker_score: bool) -> int:
		hist = self.get_hand_histogram()

		if joker_score:
			jokers = hist.get(11, 0)
			if jokers > 0 and jokers < 5:
				del hist[11]
				idx = hist.most_common(1)[0][0]
				hist[idx] += jokers

		most_common = hist.most_common()

		hand = 0
		if most_common[0][1] == 5: hand = 6
		elif most_common[0][1] == 4: hand = 5
		elif most_common[0][1] == 3 and most_common[1][1] == 2: hand = 4
		elif most_common[0][1] == 3: hand = 3
		elif most_common[0][1] == 2 and most_common[1][1] == 2: hand = 2
		elif most_common[0][1] == 2: hand = 1

		card = sum(20 ** (i + 1) * x for i, x in enumerate(reversed([ 1 if joker_score and x == 11 else x for x in self.cards ])))

		return (hand * 100_000_000) + card


	@staticmethod
	def parse(line: str):
		ranks = { 'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2 }
		x = line.split(' ')
		cards = [ ranks[c] for c in x[0] ]
		bid = int(x[1])
		return HandBid(cards, bid)

class Day7(DaySolve, TestSolve):
	def __init__(self):
		self.hands = None
		self.test_data = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

	def parse(self, data: str):
		self.hands = [ HandBid.parse(line) for line in data.splitlines() ]

	def part1(self) -> str:
		return str(sum((i + 1) * h.bid for i, h in enumerate(sorted(self.hands, key=lambda h: h.get_score(False)))))

	def part2(self) -> str:
		return str(sum((i + 1) * h.bid for i, h in enumerate(sorted(self.hands, key=lambda h: h.get_score(True)))))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '6440')

	def test2(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '5905')

	def clear(self):
		self.parsed = False

if __name__ == '__main__':
	with open('../data/input7.txt', 'r') as f:
		data = f.read()

	solver = Day7()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
