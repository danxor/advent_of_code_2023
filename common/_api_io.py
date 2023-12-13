#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os

def get_input_filename(day: int) -> str:
	day_padded = str(day).zfill(2)
	return f'data/input{day_padded}.txt'

def get_input(year: int, day: int, cookie: str) -> str:
	filename = get_input_filename(day)

	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			raw_data = f.read()
	else: 
		response = requests.get(f'https://adventofcode.com/2023/day/{day}/input', cookies={'session': cookie})
		raw_data = response.content.decode('UTF-8')
		with open(filename, 'w') as f:
			f.write(raw_data)
	return raw_data
