import traceback
import rlcompleter
import readline
readline.parse_and_bind('tab: complete')

SIZE = 3
ROW = SIZE*SIZE
unknown = '.'

#note:sub block index in the case of SIZE == 3
# +-+-+-+-+-+-+
# | 0 | 1 | 2 |
# +-+-+-+-+-+-+
# | 3 | 4 | 5 |
# +-+-+-+-+-+-+
# | 6 | 7 | 8 |
# +-+-+-+-+-+-+

def is_list_unique(l):
    """Return true if all elements in list are unique."""
    l = [v for v in l if not v is unknown]
    return len(l) == len(set(l))

def block_idx_of(x, y):
    return (x//SIZE+y//SIZE*SIZE)

class Sudoku_cell:
    def __init__(self):
        self._value = unknown
        self._candidate = set()
    def is_unknown(self):
        return self._value is unknown

    def value(self):
        return self._value
    def set_value(self, value):
        self._value = value

    def candiate(self):
        return self._candiate
    def set_candiate(self, value_set):
        self._candiate = value_set
    def remove_candiate(self, value):
        self._candiate -= set([value])
    def clone(self):
        cell = Sudoku_cell()
        cell._value = self._value
        cell._candidate = self._candidate.copy()

class Sudoku_board:
    def __init__(self):
        #Don't touch my local variables!!!!
        #Use "at" methods.

        self._cells = [Sudoku_cell() for i in range(ROW*ROW)];


    def at(self, x, y):
        return self._cells[y*ROW+x]

    def sub_row_idx(self, idx):
        """Return n-th row as list"""
        return [(i, idx) for i in range(ROW)]

    def sub_column_idx(self, idx):
        """Return n-th column as list"""
        return [(idx, i) for i in range(ROW)]

    def sub_block_idx(self, idx):
        """Return n-th block as list"""
        x_idx = [i for i in range(SIZE)]*SIZE
        #i.e. [0,1,2,0,1,2,0,1,2]
        y_idx = [i//SIZE for i in range(SIZE*SIZE)]
        #i.e. [0,0,0,1,1,1,2,2,2]

        return [(x_idx[idx]*3+x_idx[i], y_idx[idx]*3+y_idx[i]) 
                    for i in range(ROW)]

    def sub_row(self, idx):
        return [self.at(x, y) for x, y in self.sub_row_idx(idx)]
    def sub_column(self, idx):
        return [self.at(x, y) for x, y in self.sub_column_idx(idx)]
    def sub_block(self, idx):
        return [self.at(x, y) for x, y in self.sub_block_idx(idx)]

    def sub_row_values(self, idx):
        return [cell._value for cell in self.sub_row(idx)]
    def sub_column_values(self, idx):
        return [cell._value for cell in self.sub_column(idx)]
    def sub_block_values(self, idx):
        return [cell._value for cell in self.sub_block(idx)]

    def clone(self):
        """Return copy of itself"""
        new_s = Sudoku_board()
        for i in range(ROW*ROW):
            new_s._cells[i] = self._cells[i].clone()

    def is_defined(self):
        """Return true if solution have no "undefined" cell"""
        cond_list = [not cell.is_unknown() for cell in self._cells]
        #All element must be True
        return reduce(lambda x, y: x & y, cond_list)
    
    def is_acceptable(self):
        for i in range(ROW):
            if not is_list_unique(self.sub_row_values(i)):
                return False
            if not is_list_unique(self.sub_column_values(i)):
                return False
            if not is_list_unique(self.sub_block_values(i)):
                return False
        return True

    def is_legal(self):
        if not self.is_defined():
            return False

        for i in range(ROW):
            if not is_list_unique(self.sub_row_values(i)):
                return False
            if not is_list_unique(self.sub_column_values(i)):
                return False
            if not is_list_unique(self.sub_block_values(i)):
                return False
        return True

    def assign(self, x, y, value):
        """Set value at cell[x, y] and remove value from candiate
            at affected row, column, and blocks"""
        self.at(x, y).set_value(value)

        for cell in self.sub_row(y):
            cell.remove_candiate(value)
        for cell in self.sub_column(x):
            cell.remove_candiate(value)
        for cell in self.sub_block(block_idx_of(x, y)):
            cell.remove_candiate(value)
        
    def rebuild_candidate(self):
        s_row   = [set(self.sub_row_values(i))    for i in range (ROW)]
        s_column = [set(self.sub_column_values(i)) for i in range (ROW)]
        s_block  = [set(self.sub_block_values(i))  for i in range (ROW)]

        for y in range (ROW):
            for x in range (ROW):
                if self.at(x, y).is_unknown():
                    base = set(range(ROW))
                    existed  = s_row[y]|s_column[x]
                    existed |= s_block[block_idx_of(x,y)]
                    self.at(x, y).set_candiate(base-existed)
                else:
                    self.at(x, y).set_candiate(set())

    def load_from_file(self, filename):
        with open(filename) as f:
            text = f.read()
            lines = text.splitlines()
            y = 0
            for line in lines:
                if line.isspace():
                    continue
                x = 0
                for c in line:
                    if c is '.':
                        self.at(x,y).set_value(unknown)
                    elif c.isnumeric():
                        self.at(x,y).set_value(int(c) - 1)
                    else:
                        continue
                    x += 1
                y += 1
        self.rebuild_candidate()

    def funcy_print(self):
        for y in range(ROW):
            line = ""
            for x in range(ROW):
                if (x%SIZE == 0):
                    line += " "
                if self.at(x, y).is_unknown():
                    line += '.'
                else:
                    value = self.at(x, y).value() +1
                    line += str(value)
            if (y%SIZE == 0):
                print("")
            print(line)

def simple_solve_A(s):
    modified = False
    for y in range (ROW):
        for x in range (ROW):
            candiate = s.at(x, y).candiate().copy()
            if len(candiate) == 1:
                modified = True
                s.assign(x, y, candiate.pop())
    return modified

def simple_solve_B_sub(s, idx_list):
    bucket = [0 for i in range(ROW)]
    for x, y in idx_list:
        for value in s.at(x, y).candiate():
            bucket[value] += 1

    modified = False
    for x, y in idx_list:
        for value in s.at(x, y).candiate():
            if (bucket[value] == 1):
                modified = True
                s.assign(x, y, value)
                break 

    return modified

def simple_solve_B(s):
    modified = False
    for i in range(ROW):
        modified |= simple_solve_B_sub(s, s.sub_row_idx(i))
        modified |= simple_solve_B_sub(s, s.sub_column_idx(i))
        modified |= simple_solve_B_sub(s, s.sub_block_idx(i))
    return modified
 
def recursive_solve(s):
    for y in range (ROW):
        for x in range (ROW):
            if s.at(x,y) != unknown:
                continue
            for value in s.cand_at(x,y):
                clone = s.clone()
                clone.assign(x, y, value)
                result = recursive_solve(clone)
                if result:
                    return result

s = Sudoku_board()
#s.load_from_file("1_missing.dat")
s.load_from_file("lv1.dat")
s.funcy_print()
if not s.is_acceptable():
    print("fail from begining")

def run_test():
    modified = True
    while simple_solve_B(s):
        if not s.is_acceptable():
            print("fail at B")
        modified = True

    s.funcy_print()

    modified = True
    while simple_solve_A(s):
        if not s.is_acceptable():
            print("fail at A")
        modified = True

    s.funcy_print()

    modified = True
    while modified:
        modified = False
        while simple_solve_B(s):
            if not s.is_acceptable():
                print("fail at B")
            modified = True
        while simple_solve_A(s):
            if not s.is_acceptable():
                print("fail at A")
            modified = True
    s.funcy_print()

    s.rebuild_candidate()
    
    modified = True
    while modified:
        modified = False
        while simple_solve_B(s):
            if not s.is_acceptable():
                print("fail at B")
            modified = True
        while simple_solve_A(s):
            if not s.is_acceptable():
                print("fail at A")
            modified = True
    s.funcy_print()

    s.rebuild_candidate()
    
    modified = True
    while modified:
        modified = False
        while simple_solve_B(s):
            if not s.is_acceptable():
                print("fail at B")
            modified = True
        while simple_solve_A(s):
            if not s.is_acceptable():
                print("fail at A")
            modified = True
    s.funcy_print()
