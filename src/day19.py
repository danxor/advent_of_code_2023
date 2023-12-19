#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve
import re
from dataclasses import dataclass
import itertools

@dataclass
class WorkflowExpression:
	key: str
	comparison: str
	target: str

	def sets(self) -> tuple:
		if self.comparison == None:
			return (set(range(1, 4001)), set(range(1, 4001)), set(range(1, 4001)), set(range(1, 4001)))

		cmp = self.comparison[0]
		if cmp == '<':
			our = set(range(1, int(self.comparison[1:])))
		elif cmp == '>':
			our = set(range(int(self.comparison[1:]) + 1, 4001))

		match self.key:
			case 'x': return (our, set(range(1, 4001)), set(range(1, 4001)), set(range(1, 4001)))
			case 'm': return (set(range(1, 4001)), our, set(range(1, 4001)), set(range(1, 4001)))
			case 'a': return (set(range(1, 4001)), set(range(1, 4001)), our, set(range(1, 4001)))
			case 's': return (set(range(1, 4001)), set(range(1, 4001)), set(range(1, 4001)), our)

@dataclass
class Workflow:
	name: str
	expressions: list

	@staticmethod
	def parse(line: str) -> "Workflow":
		m = re.match(r'^(\w+){([^}]+)}$', line)
		if m:
			name, raw_expression = m.groups()

			expressions = []

			for expression in raw_expression.split(','):
				idx = expression.find(':')
				if idx >= 0:
					expr, target = expression.split(':')
					idx = expr.find('<')
					if idx >= 0:
						expressions.append(WorkflowExpression(expr[0:idx], expr[idx:], target))

					idx = expr.find('>')
					if idx >= 0:
						expressions.append(WorkflowExpression(expr[0:idx], expr[idx:], target))
				else:
					expressions.append(WorkflowExpression(None, None, expression))

			
			return Workflow(name, expressions)

def intersection(a: tuple, b: tuple) -> tuple:
    return tuple(itertools.starmap(set.intersection, zip(a, b)))

def subtract(a: set, b: set):
    for x, y in zip(a, b):
        if len(y) != 4000:
            x -= y

class Day19(DaySolve, TestSolve):
	def __init__(self):
		self.workflows = None
		self.part_ratings = None
		self.workflow_cases = None
		self.test_data = '''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

	def parse(self, data: str):
		raw_workflows, raw_part_ratings = data.split('\n\n')
		raw_part_ratings = raw_part_ratings.replace('{', '').replace('}', '')

		self.workflows = dict((wf.name, wf) for wf in [ Workflow.parse(line) for line in raw_workflows.splitlines() ])
		self.part_ratings = [ dict([ part.split('=') for part in line.split(',') ]) for line in raw_part_ratings.splitlines() ]
		self.workflow_cases = {}

		for wf in self.workflows.values():
			cases = []

			for expression in wf.expressions:
				sets = expression.sets()
				cases.append((expression.target, sets))

			self.workflow_cases[wf.name] = cases


	def run_workflow(self, part: dict, name: str):
		if name in self.workflows:
			wf = self.workflows[name]
			for expression in wf.expressions:
				if expression.key == None:
					return self.run_workflow(part, expression.target)
				elif expression.key in part:
					result = eval(f'{part[expression.key]}{expression.comparison}')
					if result:
						return self.run_workflow(part, expression.target)
				else:
					return None

		return name

	def workflow_combinations(self, name: str, sets: tuple) -> int:
		if not any(sets) or name == 'R':
			return 0
		elif name == 'A':
			s = 1
			for set in sets: s *= len(set)
			return s

		s = 0
		for target, restriction in self.workflow_cases[name]:
			s += self.workflow_combinations(target, intersection(sets, restriction))
			subtract(sets, restriction)

		return s

	def part1(self) -> str:
		s = 0

		for part in self.part_ratings:
			target = self.run_workflow(part, 'in')
			if target == 'A': s += sum(int(part[k]) for k in part.keys())
		
		return str(s)

	def part2(self) -> str:
		sets = (set(range(1, 4001)),  set(range(1, 4001)), set(range(1, 4001)), set(range(1, 4001)))

		return str(self.workflow_combinations('in', sets))

	def test1(self) -> tuple[str, bool]:
		self.parse(self.test_data)
		result = self.part1()
		return (result, result == '19114')

	def test2(self) -> str:
		self.parse(self.test_data)
		result = self.part2()
		return (result, result == '167409079868000')

if __name__ == '__main__':
	with open('../data/input19.txt', 'r') as f:
		data = f.read()

	solver = Day19()
	print(f'Part #1: {solver.part1(data)}')
	print(f'Part #2: {solver.part2(data)}')
