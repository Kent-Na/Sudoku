#!/usr/bin/env python
from lib.text import trim
from functools import reduce
"""
Feature: 
solve_sudoku(only one solution)
solve_sudoku(some solution)
"""

unknown = '.'
SIZE = 3
ROW  = SIZE * SIZE

def solve_sudoku(sudoku_mat):
    """
    Solve sudoku.
    return a solution of sudoku.
    """
    pass

def load_sudoku(filename):
    sudoku = [[0 for i in range(ROW)] for j in range(9)]
    with open(filename) as f:
        a_sudoku = list(trim(f.read()))
        for i,c in enumerate(a_sudoku):
            if c.isdigit() is True:
                c = int(c)
            sudoku[i // ROW][i % ROW] = c
    return sudoku

def sudoku_repr(sudoku):
    s = ''
    for row in sudoku:
        for cell in row:
            s += str(cell)
        s += '\n'
    return s


def sudoku_test():
    sudoku = load_sudoku('example.txt')
    print(sudoku_repr(sudoku))
    sol = solve_sudoku(sudoku)
    print(sudoku_repr(sol))
