#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def get_day_filename(day: int) -> str:
	day_padded = str(day).zfill(2)
	return f'src/day{day_padded}.py'

def generate_template(day: int):
	filename = get_day_filename(day)
	if os.path.isfile(filename):
		return

	with open(filename, 'w') as f:
		f.write('#!/usr/bin/env python3\n')
		f.write('# -*- coding: utf-8 -*-\n')
		f.write('\n')
		f.write('import sys\n')
		f.write('sys.path.append(\'.\')\n')
		f.write('sys.path.append(\'..\')\n')
		f.write('from common import DaySolve, TestSolve\n')
		f.write('\n')
		f.write(f'class Day{day}(DaySolve, TestSolve):\n')
		f.write('\tdef __init__(self):\n')
		f.write('\t\tself.test_data = \'\'\'\'\'\'\n')
		f.write('\n')
		f.write('\tdef parse(self, data: str):\n')
		f.write('\t\tpass\n')
		f.write('\n')
		f.write('\tdef part1(self) -> str:\n')
		f.write('\t\tpass\n')
		f.write('\n')
		f.write('\tdef part2(self) -> str:\n')
		f.write('\t\tpass\n')
		f.write('\n')
		f.write('\tdef test1(self) -> tuple[str, bool]:\n')
		f.write('\t\tself.parse(self.test_data)\n')
		f.write('\t\tresult = self.part1()\n')
		f.write('\t\treturn (result, result == \'\')\n')
		f.write('\n')
		f.write('\tdef test2(self) -> str:\n')
		f.write('\t\tself.parse(self.test_data)\n')
		f.write('\t\tresult = self.part2()\n')
		f.write('\t\treturn (result, result == \'\')\n')
		f.write('\n')
		f.write('if __name__ == \'__main__\':\n')
		f.write(f'\twith open(\'../data/input{day}.txt\', \'r\') as f:\n')
		f.write(f'\t\tdata = f.read()\n')
		f.write('\n')
		f.write(f'\tsolver = Day{day}()\n')
		f.write('\tprint(f\'Part #1: {solver.part1(data)}\')\n')
		f.write('\tprint(f\'Part #2: {solver.part2(data)}\')\n')

	files = sorted([ f for f in os.listdir('src') if f.endswith('.py') and f != '__init__.py' ])

	with open('src/__init__.py', 'w') as f:
		f.write('#!/usr/bin/env python3\n')
		f.write('# -*- coding: utf-8 -*-\n')
		f.write('\n')
		for py in [ x[:-3] for x in files ]:
			f.write(f'from .{py} import Day{int(py[3:])}\n')
