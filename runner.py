#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from common import read, get_input, generate_template, DaySolve, TestSolve
import argparse
import sys
import os
import gc

YEAR_FILE='year.txt'
COOKIE_FILE='cookie.txt'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='runner', description='Advent of Code solution runner', epilog='Copyright Daniel Andersson 2023')
	parser.add_argument('-g', '--gen', action='store_true', help='Generate code using the template and also download the input for the given days')
	parser.add_argument('-y', '--set-year', type=int, action='store', help='Stores the year to use')
	parser.add_argument('-s', '--set-cookie', type=str, action='store', help='Stores the session-cookie to use when downloading')
	parser.add_argument('-t', '--test', action='store_true', help='Run the tests associated with the given solution')
	parser.add_argument('-a', '--all', action='store_true', help='Run all the solutions up to the current day')
	parser.add_argument('-1', '--one', action='store_true', help='Run only the first star')
	parser.add_argument('-2', '--two', action='store_true', help='Run only the second star')
	parser.add_argument('integers', metavar='N', type=int, nargs='*', help='Run only the given solutions')
	args = parser.parse_args()

	if args.set_year:
		with open(YEAR_FILE, 'w') as f:
			f.write(str(args.set_year))

	try:
		with open(YEAR_FILE, 'r') as f:
			args.set_year = int(f.read())
	except FileNotFoundError:
		print('You need to run the runner with the --set-year-parameter in order to set the year-value', file=sys.stderr)
		sys.exit(1)

	if args.set_cookie:
		with open(COOKIE_FILE, 'w') as f:
			f.write(args.set_cookie)

	try:
		with open(COOKIE_FILE, 'r') as f:
			args.set_cookie = f.read()
	except FileNotFoundError:
		print('You need to run the runner with the --set-cookie-parameter in order to set the session-cookie', file=sys.stderr)
		sys.exit(1)

	today = datetime.now()
	christmas_day = datetime(args.set_year, 12, 25, 6)

	if not args.one and not args.two:
		args.one = True
		args.two = True

	if today.month < 12:
		raise ValueError('You cannot run Advent of Code until december')

	if today < christmas_day:
		if args.all:
			for d in range(1, 1 + today.day):
				args.integers.append(d)
		elif len(args.integers) == 0:
			args.integers.append(today.day)
	else:
		if args.all:
			for d in range(1, 26):
				args.integers.append(d)

	if args.gen:
		for d in args.integers:
			generate_template(d)
	else:
		for d in args.integers:
			generate_template(d)

			import src

			classes = [ attr for attr in dir(src) if isinstance(getattr(src, attr), type) ]

			if args.test:
				found = next(filter(lambda x: x == f'Day{d}', classes), None)
				if found:
					cls = getattr(src, found)
					if issubclass(cls, TestSolve):
						instance = cls()

						ans1, valid1 = instance.test1()
						print(f"Day #{d} - Part #1: {ans1} - {'Ok' if valid1 else 'Failed'}")

						ans2, valid2 = instance.test2()
						print(f"Day #{d} - Part #2: {ans2} - {'Ok' if valid2 else 'Failed'}")
			else:
				found = next(filter(lambda x: x.lower() == f'day{d}', classes), None)
				if found:
					cls = getattr(src, found)
					if issubclass(cls, DaySolve):
						data = get_input(args.set_year, d, args.set_cookie)
						if data:
							instance = cls()
							instance.parse(data)

							ans1 = instance.part1()
							print(f'Day #{d} - Part #1: {ans1}')

							ans2 = instance.part2()
							print(f'Day #{d} - Part #2: {ans2}')
				else:
						print(f'Failed to find a class which solves day {d}', file=sys.stderr)
