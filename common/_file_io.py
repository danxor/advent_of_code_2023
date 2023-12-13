#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Iterable

def read(filename: str) -> str:
	with open(filename, 'r') as f:
		return f.read()
