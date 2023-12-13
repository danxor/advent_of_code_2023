#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import runtime_checkable, Protocol

@runtime_checkable
class TestSolve(Protocol):
	def test1(self) -> tuple[str, bool]:
		pass

	def test2(self) -> tuple[str, bool]:
		pass