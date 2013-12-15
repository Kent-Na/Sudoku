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
    return len(l) == len(set(l))

class Solution:
    def __init__(self):
        #Don't touch my local variables!!!!
        #Use "at" and "set_to" methods.

        self._values = [unknown for i in range(ROW*ROW)];

    def at(self, x, y):
        return self._values[y*ROW+x]
    
    def set_to(self, x, y, value):
        self._values[y*ROW+x] = value

    def clone(self):
        """Return copy of itself"""
        new_s = Solution()
        for i in range(ROW*ROW):
            new_s._values = self._values[i]

    def is_defined(self):
        """Return true if solution have no "undefined" cell"""
        return not unknown in self._values
    
    def is_legal(self):
        if not self.is_defined():
            return False

        for i in range(ROW):
            if not is_list_unique(self.sub_row(i)):
                return False
            if not is_list_unique(self.sub_column(i)):
                return False
            if not is_list_unique(self.sub_block(i)):
                return False
        return True

    def sub_row(self, idx):
        """Return n-th row as list"""
        return [self.at(i, idx) for i in range(ROW)]

    def sub_column(self, idx):
        """Return n-th column as list"""
        return [self.at(idx, i) for i in range(ROW)]

    def sub_block(self, idx):
        """Return n-th block as list"""
        x_idx = [i for i in range(SIZE)]*SIZE
        #i.e. [0,1,2,0,1,2,0,1,2]
        y_idx = [i//SIZE for i in range(SIZE*SIZE)]
        #i.e. [0,0,0,1,1,1,2,2,2]

        return [self.at(x_idx[idx]*3+x_idx[i],y_idx[idx]*3+y_idx[i]) 
                    for i in range(ROW)]
        
class Candidate:
    def __init__(self):
        #Don't touch my local variables!!!!
        #Use "at" and "set_to" methods.

        self._values = [set() for i in range(ROW*ROW)];

    def at(self, x, y):
        return self._values[y*ROW+x]
    
    def set_to(self, x, y, value):
        self._values[y*ROW+x] = value

    def clone(self):
        """Return copy of itself"""
        new_s = Solution()
        for i in range(ROW*ROW):
            new_s._values = self._values[i]

    def sub_row(self, idx):
        """Return n-th row as list"""
        return [self.at(i, idx) for i in range(ROW)]

    def sub_column(self, idx):
        """Return n-th column as list"""
        return [self.at(idx, i) for i in range(ROW)]

    def sub_block(self, idx):
        """Return n-th block as list"""
        x_idx = [i for i in range(SIZE)]*SIZE
        #i.e. [0,1,2,0,1,2,0,1,2]
        y_idx = [i//SIZE for i in range(SIZE*SIZE)]
        #i.e. [0,0,0,1,1,1,2,2,2]

        return [self.at(x_idx[idx]*3+x_idx[i],y_idx[idx]*3+y_idx[i]) 
                    for i in range(ROW)]

def block_idx_of(x, y):
    return (x//ROW+y//ROW*ROW)

def make_candidate_from_solution(s):
    s_rows   = [set(s.sub_row(i))    for i in range (ROW)]
    s_column = [set(s.sub_column(i)) for i in range (ROW)]
    s_block  = [set(s.sub_block(i))  for i in range (ROW)]

    c = Candidate()
    for y in range (ROW):
        for x in range (ROW):
            base = set(range(ROW))
            existed = s_rows[x]|s_column[y]|s_block[block_idx_of(x,y)]
            Candidate.set_to(x, y, base-existed)

def simple_solve(s):
    c = make_candidate_from_solution(s)
    for y in range (ROW):
        for x in range (ROW):
            if len(c.at(x, y)) == 1:
                _assign(s, c, x, y, c.at(x, y).pop())
 
def rec_solve(s):
    for y in range (ROW):
        for x in range (ROW):
            if s.at(x,y) != unknown:
                continue
            for value in s.cand_at(x,y):
                clone = s.clone()
                clone.assign(x, y, value)
                result = rec_solve(clone)
                if result:
                    return result
