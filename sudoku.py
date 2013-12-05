#!/usr/bin/env python3
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
    
    try:
        sol = sol_candidates.pop()
    except KeyError:
        print(unknown)
        print(sudoku_mat[i][j])

    return sol

def solverule2(sudoku_mat,i,j):
    """
    column check.
    """
    sudoku_mat = sudoku_mat[:][:]
    if sudoku_mat[i][j] != unknown:
        return None

    column_set = set([sudoku_mat[k][j] for k in range(ROW)])
    sol_candidates = set(range(1,10)).difference(set(column_set))
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

    cell_set = set([sudoku_mat[i//3 * 3 + k][j//3 * 3 + l] \
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
    is_finished = False
    
    while not defined_matrix(sudoku_mat) and not is_finished:
        old_mat = sudoku_mat
        for i in range(ROW):
            for j in range(ROW):
                if sudoku_mat[i][j] != unknown: # case defined
                    continue
                for rule in solve_rules:
                    sol = rule(sudoku_mat, i, j)
                    if not sol in (None, False):
                        sudoku_mat[i][j] = sol
                        print('define {},{}'.format(i,j))
        if old_mat == sudoku_mat:
            is_finished = True
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

def main(filename):
    sudoku = load_sudoku(filename)
    print('give: ' + '=' * 9)
    print(sudoku_repr(sudoku))
    
    sol = solve_sudoku(sudoku)
    print()
    if not defined_matrix(sol):
        print('The question can\'t solved.')
    print('solution:' + '=' * 9)
    print()
    print(sudoku_repr(sol))

def sudoku_test():
    main('example.dat')

if __name__ == '__main__':
    is_test = False
    
    if is_test:
        sudoku_test()
    else:
        from sys import argv
        filename = argv[1]
        main(filename)
