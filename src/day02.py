#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
from dataclasses import dataclass
from collections import Counter
import re

@dataclass
class Game:
		game_id: int
		cubes: list[Counter]

		@staticmethod
		def parse(line: str) -> "Game":
			parts = line.split(': ')
			game_id = int(parts[0][5:])

			cubes = []
			for subset in parts[1].split(';'):
				counter = Counter()
				for count, color in re.findall(r'(\d+) (\w+)', subset):
					counter[color] = int(count)
				cubes.append(counter)

			return Game(game_id, cubes)

class Day2(DaySolve, TestSolve):
	def __init__(self):
		self.games = None
		self.test_data = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

	def parse(self, data: str):
		self.games = [ Game.parse(line) for line in data.splitlines() ]

	def part1(self) -> str:
				color_max = { 'red': 12, 'green': 13, 'blue': 14 }

				s = 0

				for game in self.games:
						valid = True

						for cubes in game.cubes:
								for color in color_max.keys():
										if cubes[color] > color_max[color]:
											valid = False
											break

						if valid: s += game.game_id

				return str(s)

	def part2(self) -> str:
				s = 0
				
				for game in self.games:
						set_max  = { 'red': 0, 'green': 0, 'blue': 0 }
						for cubes in game.cubes:
								for color in set_max.keys():
										if cubes[color] > set_max[color]:
												set_max[color] = cubes[color]

						s += set_max['red'] * set_max['green'] * set_max['blue']

				return str(s)

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '8')

	def test2(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '2286')

	def clear(self):
		self.parsed = False

if __name__ == '__main__':
	with open('data/input2.txt', 'r') as f:
		data = f.read()

	solver = Day2()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
