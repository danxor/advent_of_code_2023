#!/usr/bin/env python3

from typing import Callable, Generic, List, Tuple, TypeVar
import heapq

T = TypeVar('T')

class Map(Generic[T]):
	@staticmethod
	def from_lines(lines: List[str], transpose: Callable[[T], int] = lambda x: x):
		m = Map(len(lines[0]), len(lines))
		for r in range(m.height):
			for c in range(m.width):
				m[(c, r)] = transpose(lines[r][c])
		return m

	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height
		self.nodes = [ 0 ] * self.width * self.height

	def __getitem__(self, key: Tuple[int, int]) -> T:
		x, y = key
		if 0 <= x < self.width and 0 <= y < self.height:
			return self.nodes[x + self.width * y]
		return None

	def __setitem__(self, key: Tuple[int, int], value: T):
		x, y = key
		if 0 <= x < self.width and 0 <= y < self.height:
			self.nodes[x + self.width * y] = value
		else:
			raise ValueError(f'Location is not inside map: {x},{y}')

	def __contains__(self, key: Tuple[int, int]) -> bool:
		return 0 <= key[0] < self.width and 0 <= key[1] < self.height

	def find(self, value: T) -> Tuple[int, int]:
		possible = self.findall(value)
		if len(possible) == 1:
			return possible[0]
		else:
			raise ValueError(f'Failed to find a single {value}: {possible}')

	def findall(self, value: T) -> List[Tuple[int, int]]:
		return [ (x[0] % self.width, x[0] // self.width) for x in filter(lambda e: e[1] == value, enumerate(self.nodes)) ]

	def successors4(self, n: Tuple[int, int]) -> List[Tuple[int, int]]:
		for k in [ (n[0] + 1, n[1]), (n[0] - 1, n[1]), (n[0], n[1] + 1), (n[0], n[1] - 1) ]:
			if k in self:
				yield k

	def successors8(self, n: Tuple[int, int]) -> List[Tuple[int, int]]:
		for k in [ (n[0] - 1, n[1] - 1), (n[0], n[1] - 1), (n[0] + 1, n[1] - 1), (n[0] - 1, n[1]), (n[0] + 1, n[1]), (n[0] - 1, n[1] + 1), (n[0], n[1] + 1), (n[0] + 1, n[1] + 1) ]:
			if k in self:
				yield k

	def a_star(self, start: T | Tuple[int, int], end: T | Tuple[int, int] | Callable[[Tuple[int, int]], bool], successors: Callable[[Tuple[int, int]], List[Tuple[int, int]]], heuristic: Callable[[Tuple[int, int]], int] = lambda p: 0) -> Tuple[List[Tuple[int, int]], int, int]:
		queue = [(heuristic(start), start)]
		paths = {}
		costs = { start: 0 }
		total = 0

		if type(start) is not tuple:
			start = map.find(start)

		if callable(end):
			is_end = end
		elif type(end) is tuple:
			single_end = end
			def is_end(e: Tuple[int, int]) -> bool:
				return e == single_end
		else:
			single_end = end
			def is_end(e: Tuple[int, int]) -> bool:
				return self[e] == single_end

		while queue:
			total += 1
			cost, cur = heapq.heappop(queue)

			if is_end(cur):
				path = [cur]
				print(f'{path}')
				while cur in paths:
					print(f'{cur}')
					cur = paths[cur]
					path.append(cur)
					cost -= heuristic(cur)
				return (path[::-1], cost, total)

			for step in successors(cur):
				adj, step_cost = step, 1
				adj_cost = cost + step_cost
				if adj not in costs or adj_cost < costs[adj]:
					paths[adj] = cur
					costs[adj] = adj_cost
					heapq.heappush(queue, (adj_cost + heuristic(adj), adj))

		return None
