#!/usr/bin/env python3
from lib.text import trim
from copy import deepcopy
from functools import reduce
import pickle
from sys import exit
"""
Feature: 
solve_sudoku(only one solution)
solve_sudoku(some solution)
"""

# global variables 
unknown = '.'
SIZE = 3
ROW  = SIZE * SIZE
sudoku_ans_filename = 'sudoku_anses.pkl'

### basic functions

def clone_sudoku(sudoku):
    return [[sudoku[j][i] for i in range(ROW)] for j in range(ROW)]

def defined_matrix(sudoku_mat):
    sudoku_mat = clone_sudoku(sudoku_mat)
    return not unknown in \
            [sudoku_mat[i][j] for i in range(ROW) for j in range(ROW)]

def is_legal_matrix(sudoku_mat):
    if not defined_matrix(sudoku_mat):
        return False
    
    # vertical check
    for i in range(ROW):
        if set(sudoku_mat[i]) != set(range(1,10)):
            #print(sudoku_mat[i])
            return False

    # yoko check
    for j in range(ROW):
        if set([sudoku_mat[i][j] for i in range(ROW)]) != set(range(1,ROW + 1)):
            return False

    # Cell check
    for i in range(SIZE):
        for j in range(SIZE):
            if set([sudoku_mat[3*i + k][3 * j + l] \
                    for k in range(SIZE) for l in range(SIZE)]) \
                    != set(range(1, ROW + 1)):
                return False
    return True

def get_candidates(sudoku,i,j):
    """
    return cadidate at sudoku.(i,j)
    if sudoku.(i,j) is defined, return None.
    """
    sudoku = clone_sudoku(sudoku)
    if sudoku[i][j] != unknown:
        return None

    candidates = set(range(1,10))
    vertical = set(sudoku[i])
    yoko     = set([sudoku[k][j] for k in range(ROW)])
    cell     = set([sudoku[i//3*3 + k][j//3*3 + l]\
                for k in range(SIZE) for l in range(SIZE)])
    candidates = candidates.difference(vertical)
    candidates = candidates.difference(yoko)
    candidates = candidates.difference(cell)
    return candidates

def get_all_candidates(sudoku):
    """
    """
    d_candidates = {}
    for i in range(ROW):
        for j in range(ROW):
            candidates = get_candidates(sudoku, i, j)
            if candidates:
                d_candidates[(i,j)] = candidates

    return d_candidates

### solve

## for basic solve
def solverule1(sudoku_mat,i,j):
    """
    row check.
    If this function returned False, we didn't solve.
    If I this function returned None, we sudoku_mat[i][j] is defined.
    else we give solution at (i,j).
    """
    sudoku_mat = clone_sudoku(sudoku_mat)
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
    sudoku_mat = clone_sudoku(sudoku_mat)
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
    sudoku_mat = clone_sudoku(sudoku_mat)
    
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

def solve_basic_sudoku(sudoku_mat):
    """
    Solve sudoku.
    return a solution of sudoku.
    """
    sudoku_mat = clone_sudoku(sudoku_mat)
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
                        #print('define {},{}'.format(i,j))
        if old_mat == sudoku_mat:
            is_finished = True
    return sudoku_mat

## solve by recursive method

def solve_sudoku_by_recursive(sudoku, cnt=0):  # todo: with mistake?
    #print(sudoku)
    sudoku = clone_sudoku(sudoku)
    #print(sudoku)

    d_candiate = get_all_candidates(sudoku)
    if len(d_candiate) == 0:
        if is_legal_matrix(sudoku):
            return sudoku
        else:
            #print(sudoku_repr(sudoku))
            return None

    undef_ind, candiates = list(d_candiate.items())[0]
    if cnt < 10:
        print('{}th loop is started.'.format(cnt))
    for candiate in candiates:
        sol = [[sudoku[j][i] for i in range(ROW)] for j in range(ROW)]
        sol[undef_ind[0]][undef_ind[1]] = candiate

        sol = solve_basic_sudoku(sol)
        sol = solve_sudoku_by_recursive(sol, cnt=cnt+1)

        if sol==None:
            continue
        
        if is_legal_matrix(sol):
            return sol
        elif defined_matrix(sol):
            print("This question has no solution.")
    if cnt < 10:
        print('{}th loop is finished.'.format(cnt))
    return None
        
def solve_sudoku(sudoku):
    sudoku = clone_sudoku[sudoku_mat]
    sudoku = solve_basic_sudoku(sudoku)
    return solve_sudoku_by_recursive(sudoku)

### functions for main
                
def load_sudoku(filename):
    sudoku = [[0 for i in range(ROW)] for j in range(ROW)]
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

def is_legal_test():
    filename = 'ans.dat'
    sudoku = load_sudoku(filename)
    print(is_legal_matrix(sudoku))

### main
def main(filename):
    sudoku = load_sudoku(filename)
    print('give: ' + '=' * 9)
    print(sudoku_repr(sudoku))
    
    sol = solve_sudoku_by_recursive(sudoku)
    if not is_legal_matrix(sol):
        print('The question can\'t solved.')
    else:
        print('solution:' + '=' * 9)
        print(sudoku_repr(sol))

def sudoku_test():
    main('difficult.dat')

if __name__ == '__main__':
    is_test = False
    
    if is_test:
        sudoku_test()
    else:
        from sys import argv
        filename = argv[1]
        main(filename)
