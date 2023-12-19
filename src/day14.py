#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
sys.path.append('..')
from common import DaySolve, TestSolve

def tilt(board: list) -> list:
    oup = [['.' for _ in range(len(board[0]))] for _ in range(len(board))]
    for j in range(0, len(board[0])):
        roll_to = 0
        for i in range(0, len(board)):
            curr_square = board[i][j]
            if curr_square == '.':
                pass
            if curr_square == '#':
                oup[i][j] = '#'
                roll_to = i + 1
            if curr_square == 'O':
                oup[roll_to][j] = 'O'
                roll_to = roll_to + 1

    return oup

def rotate(board: list) -> list:
    return list(zip(*board[::-1]))

def cycle(board: list) -> list:
    new_board = board

    for i in range(4):
        new_board = tilt(new_board)
        new_board = rotate(new_board)
    
    return new_board

def score(board: list) -> int:
    max_y = len(board)

    total = 0
    for y, line in enumerate(board):
        for ch in line:
            if ch == 'O':
                total += max_y - y

    return total

class Day14(DaySolve, TestSolve):
        def __init__(self):
                self.board = None
                self.test_data = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

        def parse(self, data: str):
                self.board = []
                for line in data.splitlines():
                        self.board.append(list(line.strip()))

        def part1(self) -> str:
                new_board = tilt(self.board)
                return str(score(new_board))

        def part2(self) -> str:
                kept_boards = []

                new_board = self.board

                target = 1_000_000_000
                for i in range(target):
                    b = [ ''.join([ c for c in line ]) for line in new_board ]
                    if b in kept_boards:
                        idx = kept_boards.index(b)
                        cycle_len = len(kept_boards) - idx
                        found = kept_boards[idx + ((target - i) % cycle_len)]
                        return str(score(found))
                    else:
                        kept_boards.append(b)
                        new_board = cycle(new_board)

                return None

        def test1(self) -> tuple[str, bool]:
                self.parse(self.test_data)
                result = self.part1()
                return (result, result == '136')

        def test2(self) -> str:
                self.parse(self.test_data)
                result = self.part2()
                return (result, result == '64')

if __name__ == '__main__':
        with open('../data/input14.txt', 'r') as f:
                data = f.read()

        solver = Day14()
        print(f'Part #1: {solver.part1(data)}')
        print(f'Part #2: {solver.part2(data)}')
