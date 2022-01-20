
WIDTH = 8
HEIGHT = 8

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

class Board:
    def __init__(self, height = HEIGHT, width = WIDTH):
        self.height = height
        self.width = width
        self.size = height, width
        self.grid =  []
        self.free_cells = height * width

        for rownum in range(height):
            row = []
            self.grid.append(row)
            for colnum in range(width):
                liberties = 2
                if rownum > 0 and rownum < height - 1:
                    liberties += 1
                if colnum > 0 and colnum < width - 1:
                    liberties += 1
                row.append(Cell((rownum, colnum), liberties))

        h,w = height, width
        for rownum in range(height):
            for colnum in range(width):
                cell = self.grid[rownum][colnum]
                r,c = cell.pos

                for dr,dc in [(-1,0),(0,1),(1,0),(0,-1)]:
                    if 0 <= r+dr < h and 0 <= c+dc < w:
                        cell.adjacent_cells.append(self.grid[r+dr][c+dc])
        
    def set_value(self, pos, value):
        h,w = self.size
        #print("setting", pos, value)
        if not 0 <= pos[0] < h or not 0 <= pos[1] < w:
            raise Exception("refusing to set invalid pos", pos)
        cell = self.get_cell(pos)
        if cell.value is not None:
            raise Exception("value already set")
        self.free_cells -= 1

        cell.value = value
        for adjacent in cell.adjacent_cells:
            adjacent.liberties -= 1

    def clear_value(self, pos):
        cell = self.get_cell(pos)
        self.free_cells += 1

        cell.value = None
        for adjacent in cell.adjacent_cells:
            adjacent.liberties += 1

    def get_horse_values(self, pos):
        r,c = pos
        h,w = self.size

        for dr, dc in [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]:
            if 0 <= r+dr < h and 0 <= c+dc < w:
                v = self.grid[r+dr][c+dc].value
                if v is not None:
                    yield v
      
        return

    def get_cell(self, pos):
        r,c = pos
        return self.grid[r][c]
      
    def count_free(self):
        return self.free_cells

    def has_split_regions(self):
        return False

    def show_path(self, start, moves):
        south = set() #set of cells with a south link
        east = set() #set of cells with a east link
        current = start
        for m in moves:
            if m.name == NORTH:
                current = current[0]-1, current[1]
                south.add(current)
            elif m.name == SOUTH:
                south.add(current)
                current = current[0]+1, current[1]
            elif m.name == WEST:
                current = current[0], current[1]-1
                east.add(current)
            elif m.name == EAST:
                east.add(current)
                current = current[0], current[1]+1

        result = ""
        for row in self.grid:
            for cell in row:
                cell_value = str(cell.value) if cell.value is not None else '_'
                #result += "%s (%s)"%(cell_value, cell.liberties)
                result += cell_value
                result += '--' if cell.pos in east else '  '
            result += "\n"
            for cell in row:
                result += '|' if cell.pos in south else ' '
                result += '  '
                #result += '      '
            result += "\n"
        return result


class Cell:
    def __init__(self, pos, liberties):
        self.pos = pos
        self.liberties = liberties

        self.value = None
        self.adjacent_cells = []

    def is_set(self): 
        return self.value is not None

    def has_adjacent_cell_without_liberties(self):
        for a in self.adjacent_cells:
            if a.liberties == 0:
                return True

        return False

class Move:
    def __init__(self, name, position_delta):
        self.name = name
        self.position_delta = position_delta

    def is_valid(self, board, die):
        pos = (die.pos[0] + self.position_delta[0], die.pos[1] + self.position_delta[1])
        r,c = pos

        if not self.is_inside_board((r,c), board.size):
            return False

        cell = board.get_cell(pos)
        if cell.is_set():
            return False

        #print("rolling ", self.name)
        die.roll(self)

        if die.top in board.get_horse_values(die.pos):
            #print("horse violation, rolling back ", OPPOSITE[self].name)
            die.roll(OPPOSITE[self])
            return False

        #print("valid roll, rolling back ", OPPOSITE[self].name)
        die.roll(OPPOSITE[self])
        return True

    def is_inside_board(self, pos, boardsize):
        r,c = pos
        h,w = boardsize
        return 0 <= r < h and 0 <= c < w
          
    def apply(self, board, die):
        die.roll(self)
        board.set_value(die.pos, die.top)

    def revert(self, board, die):
        board.clear_value(die.pos)
        die.roll(OPPOSITE[self])
        

MOVE_NORTH = Move(NORTH, (-1,0))
MOVE_SOUTH = Move(SOUTH, (1,0))
MOVE_EAST = Move(EAST, (0,1))
MOVE_WEST = Move(WEST, (0,-1))

MOVES = [
  MOVE_NORTH, MOVE_EAST, MOVE_SOUTH, MOVE_WEST
]

OPPOSITE = {
  MOVE_NORTH: MOVE_SOUTH,
  MOVE_SOUTH: MOVE_NORTH,
  MOVE_EAST: MOVE_WEST,
  MOVE_WEST: MOVE_EAST,
}

class Die:
    def __init__(self, startpos = (1,3)):
      self.top = 6 
      self.front = 2 
      self.right = 4
      self.bottom = 1
      self.back = 5
      self.left = 3

      self.pos = startpos

    def roll(self, move):
        if move.name == NORTH:
            self.top, self.back, self.bottom, self.front = self.front, self.top, self.back, self.bottom
        elif move.name == SOUTH:
            self.top, self.front, self.bottom, self.back = self.back, self.top, self.front, self.bottom
        elif move.name == EAST:
            self.top, self.left, self.bottom, self.right = self.left, self.bottom, self.right, self.top
        elif move.name == WEST:
            self.top, self.left, self.bottom, self.right = self.right, self.top, self.left, self.bottom
        else:
            raise Exception("invalid move"%(move))

        self.pos = (self.pos[0] + move.position_delta[0], self.pos[1] + move.position_delta[1])


def main():
    board = Board(HEIGHT, WIDTH)
    die = Die()
    
    return solve(board, die)

def solve(board, die):
    board.set_value(die.pos, die.top)
    return solve_recursive(board, die, [])

best = 100
def solve_recursive(board, die, moves = []):
    global best

    if board.free_cells == 0:
        print("found a solution")

        for row in board.grid:
            print([ c.value for c in row])

        print(board.show_path((1,3),moves))

        print("moves")
        print([m.name for m in moves])

        print("total", sum([sum([c.value for c in row]) for row in board.grid]))
        return moves

    if board.free_cells < best:
        best = board.free_cells
        print("best free_cells:", best)
        print([m.name for m in moves])
        print(board.show_path((1,3), moves))


    candidate_moves = MOVES

    # Avoid cutting of cells (TODO: can we find an efficient wayt to avoid cutting of entire groups of cells?)
    adjacent_no_liberties = list(filter(lambda c: c.value is None and c.liberties == 0, board.get_cell(die.pos).adjacent_cells))
    if len(adjacent_no_liberties) > 1:
        candidate_moves = []
    if len(adjacent_no_liberties) == 1:
        cut_off_cell = adjacent_no_liberties[0]
        candidate_moves = [determine_move(die.pos, cut_off_cell.pos)]
        #print("only one candidate move:", candidate_moves[0].name)

    for move in candidate_moves:
        if not move.is_valid(board, die):
            continue

        else:
            move.apply(board, die)
            if not board.has_split_regions():
                moves.append(move)
                result = solve_recursive(board, die, moves)
                if result is not None:
                    return result
                moves.pop()
            move.revert(board, die)

    return None

MOVES_BY_OFFSET = dict()
MOVES_BY_OFFSET[(-1,0)] = MOVE_NORTH
MOVES_BY_OFFSET[(1,0)] = MOVE_SOUTH
MOVES_BY_OFFSET[(0,-1)] = MOVE_WEST
MOVES_BY_OFFSET[(0,1)] = MOVE_EAST

def determine_move(a, b):
    dr, dc = b[0]-a[0], b[1]-a[1]
    return MOVES_BY_OFFSET[(dr, dc)]

if __name__=="__main__":
    main()
