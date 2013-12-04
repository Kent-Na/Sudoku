#!/usr/bin/env python
from lib.text import trim
from functools import reduce
from sys import exit
"""
Feature: 
solve_sudoku(only one solution)
solve_sudoku(some solution)
"""

unknown = '.'
SIZE = 3
ROW  = SIZE * SIZE

def defined_matrix(sudoku_mat):
    sudoku_mat = sudoku_mat[:][:]
    return not unknown in \
            [sudoku_mat[i][j] for i in range(ROW) for j in range(ROW)]

def solverule1(sudoku_mat,i,j):
    """
    row check.
    If this function returned False, we didn't solve.
    If I this function returned None, we sudoku_mat[i][j] is defined.
    else we give solution at (i,j).
    """
    sudoku_mat = sudoku_mat[:][:]
    if sudoku_mat[i][j] != unknown:
        return None

    sol_candidates = set(range(1,10)).difference(set(sudoku_mat[i]))
    if len(sol_candidates) >= 2:    # case: unknown
        return False
    
    sol = sol_candidates.pop()
    return sol

def solverule2(sudoku_mat,i,j):
    """
    column check.
    """
    sudoku_mat = sudoku_mat[:][:]
    if sudoku_mat[i][j] != unknown:
        return None

    sol_candidates = set(range(1,10)).difference(set(sudoku_mat[:][j]))
    if len(sol_candidates) >= 2:    # case: unknown
        return False

    sol = sol_candidates.pop()
    return sol

def solverule3(sudoku_mat,i,j):
    """
    cell check
    """
    sudoku_mat = sudoku_mat[:][:]
    if sudoku_mat[i][j] != unknown:
        return None

    cell_set = set([sudoku[i//3 + k][j//3 + l] \
            for k in range(3) for l in range(3)])
    sol_candidates = set(range(1,10)).difference(cell_set)
    if len(sol_candidates) >= 2:
        return False

    sol = sol_candidates.pop()
    return sol

solve_rules = (solverule1, solverule2, solverule3)

def solve_sudoku(sudoku_mat):
    """
    Solve sudoku.
    return a solution of sudoku.
    """
    sudoku_mat = sudoku_mat[:][:]
    
    while not defined_matrix(sudoku_mat):
        for i in range(ROW):
            for j in range(ROW):
                if sudoku_mat[i][j] != unknown: # case defined
                    continue
                for rule in solve_rules:
                    sol = rule(sudoku_mat, i, j)
                    if not sol in (None, False):
                        sudoku_mat[i][j] = sol
        print(sudoku_mat)
    return sudoku_mat

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
    sudoku = load_sudoku('easy_quiestion.dat')
    print(sudoku_repr(sudoku))
    sol = solve_sudoku(sudoku)
    print(sudoku_repr(sol))

sudoku_test()
