#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import runtime_checkable, Protocol

@runtime_checkable
class DaySolve(Protocol):
	def parse(self, data: str):
		pass

	def part1(self) -> str:
		pass

	def part2(self) -> str:
		pass

