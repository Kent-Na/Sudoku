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

def clone_sudoku(sudoku_mat):
    return [[sudoku_mat[j][i] for i in range(ROW)] for j in range(ROW)]

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

def get_candidates(sudoku_mat,i,j):
    """
    return cadidate at sudoku_mat.(i,j)
    if sudoku_mat.(i,j) is defined, return None.
    """
    sudoku_mat = clone_sudoku(sudoku_mat)
    if sudoku_mat[i][j] != unknown:
        return None

    candidates = set(range(1,10))
    vertical = set(sudoku_mat[i])
    yoko     = set([sudoku_mat[k][j] for k in range(ROW)])
    cell     = set([sudoku_mat[i//3*3 + k][j//3*3 + l]\
                for k in range(SIZE) for l in range(SIZE)])
    candidates = candidates.difference(vertical)
    candidates = candidates.difference(yoko)
    candidates = candidates.difference(cell)
    return candidates

def get_all_candidates(sudoku_mat):
    """
    """
    d_candidates = {}
    for i in range(ROW):
        for j in range(ROW):
            candidates = get_candidates(sudoku_mat, i, j)
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

def solve_simple_sudoku(sudoku_mat):
    print("I'm here!!")
    print(sudoku_repr(sudoku_mat))
    sudoku_mat = clone_sudoku(sudoku_mat)
    d_candiates = get_all_candidates(sudoku_mat)

    # if number of candiate == 1, decide at this point.
    for undef_ind in d_candiates:
        if len(d_candiates[undef_ind]) == 1:
            i, j = undef_ind
            candiate = d_candiates[undef_ind].pop()
            sudoku_mat[i][j] = candiate
            print('Tester')
            return solve_simple_sudoku(sudoku_mat)

    for undef_ind in d_candiates:
        i, j = undef_ind
        undef_set = d_candiates[undef_ind]
        
        vertical_defined_set = set()
        for l in range(ROW):
            if  l != j and (i,l) in d_candiates:
                vertical_defined_set = vertical_defined_set.union(d_candiates[(i,l)])
        for candiate in d_candiates[undef_ind]:
            if not candiate in vertical_defined_set:
                sudoku_mat[i][j] = candiate
                return solve_simple_sudoku(sudoku_mat)
        undef_set = d_candiates[undef_ind]
        
        horizontan_defined_set = set()
        for k in range(ROW):
            if k != i and (k,j) in d_candiates:
                horizontan_defined_set = horizontan_defined_set.union(d_candiates[(k,j)])
        for candiate in d_candiates[undef_ind]:
            if not candiate in horizontan_defined_set:
                sudoku_mat[i][j] = candiate
                return solve_simple_sudoku(sudoku_mat)
        undef_set = d_candiates[undef_ind]

        cell_defined_set = set()
        for k in range(SIZE):
            for l in range(SIZE):
                if (i//3*3 + k != i and j//3*3 + l != j) and \
                        (i//3*3 + k, j//3*3+l) in d_candiates[undef_ind]:
                    cell_defined_set = cell_defined_set.union(
                            d_candiates[(i//3*3+k)][j//3*3+k])
        for candiate in d_candiates[undef_ind]:
            if not candiate in cell_defined_set:
                sudoku_mat[i][j] = candiate
                return solve_simple_sudoku(sudoku_mat)
    print(sudoku_repr(sudoku_mat))
    return sudoku_mat
                
def solve_basic_sudoku(sudoku_mat):
    """
    Solve sudoku_mat.
    return a solution of sudoku_mat.
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
    return solve_simple_sudoku(sudoku_mat)

## solve by recursive method

def solve_sudoku_by_recursive(sudoku_mat, cnt=0):  # todo: with mistake?
    print('Recursive')
    sudoku_mat = clone_sudoku(sudoku_mat)
    #print(sudoku_mat)

    d_candiate = get_all_candidates(sudoku_mat)
    if len(d_candiate) == 0:
        if is_legal_matrix(sudoku_mat):
            return sudoku_mat
        else:
            #print(sudoku_repr(sudoku_mat))
            return None

    undef_ind, candiates = list(d_candiate.items())[0]
    if cnt < 20:
        print('{}th loop is started.'.format(cnt))
    for candiate in candiates:
        sol = [[sudoku_mat[j][i] for i in range(ROW)] for j in range(ROW)]
        sol[undef_ind[0]][undef_ind[1]] = candiate

        sol = solve_basic_sudoku(sol)
        sol = solve_sudoku_by_recursive(sol, cnt=cnt+1)

        if sol==None:
            continue
        
        if is_legal_matrix(sol):
            return sol
        elif defined_matrix(sol):
            print("This question has no solution.")
    if cnt < 20:
        print('{}th loop is finished.'.format(cnt))
    return None
        
def solve_sudoku(sudoku_mat):
    sudoku_mat = clone_sudoku(sudoku_mat)
    sudoku_mat = solve_basic_sudoku(sudoku_mat)
    return solve_sudoku_by_recursive(sudoku_mat)

### functions for main
                
def load_sudoku(filename):
    sudoku_mat = [[0 for i in range(ROW)] for j in range(ROW)]
    with open(filename) as f:
        a_sudoku = list(trim(f.read()))
        for i,c in enumerate(a_sudoku):
            if c.isdigit() is True:
                c = int(c)
            sudoku_mat[i // ROW][i % ROW] = c
    return sudoku_mat

def sudoku_repr(sudoku_mat):
    s = ''
    for row in sudoku_mat:
        for cell in row:
            s += str(cell)
        s += '\n'
    return s

def is_legal_test():
    filename = 'ans.dat'
    sudoku_mat = load_sudoku(filename)
    print(is_legal_matrix(sudoku_mat))

### main
def main(filename):
    sudoku_mat = load_sudoku(filename)
    print('give: ' + '=' * 9)
    print(sudoku_repr(sudoku_mat))
    
    sol = solve_sudoku_by_recursive(sudoku_mat)
    if not is_legal_matrix(sol):
        print('The question can\'t solved.')
    else:
        print('solution:' + '=' * 9)
        print(sudoku_repr(sol))

def sudoku_test():
    main('difficult.dat')

def solve_simple_sudoku_test():
    sudoku_mat = load_sudoku('easy_question.dat')
    print(sudoku_repr(solve_simple_sudoku(sudoku_mat)))

if __name__ == '__main__':
    is_test = False
    
    if is_test:
        sudoku_test()
    else:
        from sys import argv
        filename = argv[1]
        main(filename)
