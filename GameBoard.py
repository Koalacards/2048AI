import random
import math
import itertools
from PerfTimer import perf_timer

CELL_WIDTH = 7
CELL_HEIGHT = 3
BASE_NUMBER = 2
GRID_SIZE = 4
PLAYER_ACTIONS = ['up', 'down', 'left', 'right']

row_left_perms = {} # map row to left shift performed on row
row_right_perms = {} # map row to right shift performed on row

def find_first_left(row_copy, col) -> tuple[int, int]:
    """
    Returns a tuple of the value of the first non-empty cell to the left of the given one,
        and the column index of that cell.
        Returns None if no cell found.
    """
    for i in range(col-1, -1, -1):
        if row_copy[i] is not None:
            return (row_copy[i], i)
    return None

# fill out left and right shift maps (used for more efficient game logic)

for row in itertools.product(*[range(18)]*4):
    tiles = []
    for num in row:
        if num == 0:
            tiles.append(None)
        else:
            tiles.append(2**num)
    
    row_copy = [None] * GRID_SIZE
    changed = False
    score_add = 0

    for col in range(GRID_SIZE):
        if tiles[col] is None:
            continue
        if col == 0:
            row_copy[col] = tiles[col]
            continue
        first_left = find_first_left(row_copy, col)
        if first_left is None:
            changed = True
            row_copy[0] = tiles[col]
        elif first_left[0] == tiles[col]:
            changed = True
            row_copy[first_left[1]] *= -2
            score_add += tiles[col] * 2
        elif first_left[1] < col - 1:
            changed = True
            row_copy[first_left[1] + 1] = tiles[col]
        else:
            row_copy[col] = tiles[col]

    new_row = [None] * GRID_SIZE
    for col in range(GRID_SIZE):
        if row_copy[col] is None:
            new_row[col] = None
        else:
            new_row[col] = abs(row_copy[col])
    
    row_left_perms[tuple(tiles)] = (new_row, changed, score_add)
    row_right_perms[tuple(reversed(tiles))] = (list(reversed(new_row)), changed, score_add)

def row_left(row):
    """
    Given an array representing a row, perform a left shift on it.
    """
    new_row, changed, score_add = row_left_perms[tuple(row)]
    return new_row.copy(), changed, score_add

def row_right(row):
    """
    Given an array representing a row, perform a right shift on it.
    """
    new_row, changed, score_add = row_right_perms[tuple(row)]
    return new_row.copy(), changed, score_add

class GameBoard():
    def __init__(self, add_tiles = True) -> None:
        self.score = 0

        # generate empty board
        self.spaces = [[None] * GRID_SIZE for i in range(GRID_SIZE)]

        # add two numbers to random spots on grid
        if add_tiles:
            self.add_random_tile()
            self.add_random_tile()

    def copy(self):
        new_board = GameBoard(False)
        new_board.score = self.score
        for i in range(len(self.spaces)):
            new_board.spaces[i] = self.spaces[i].copy()
        return new_board
    
    def hash_board(self):
        return str(self.spaces)

    def __repr__(self):
        # print top lines and first row of numbers/spaces
        out = self.top_lines()
        for i in range(math.ceil((CELL_HEIGHT - 1) / 2)):
            out += self.space_lines()
        out += self.row_str(0)
        for i in range(math.floor((CELL_HEIGHT - 1) / 2)):
            out += self.space_lines()

        # print all grid lines and all remaining cells
        for i in range(1, GRID_SIZE):
            out += self.grid_lines()
            for j in range(math.ceil((CELL_HEIGHT - 1) / 2)):
                out += self.space_lines()
            out += self.row_str(i)
            for j in range(math.floor((CELL_HEIGHT - 1) / 2)):
                out += self.space_lines()

        # print bottom row of lines
        out += self.bottom_lines()

        # print current game score
        out += f"Score: {self.score}"
        return out
    
    def top_lines(self):
        return '\u250C' + (GRID_SIZE - 1) * (CELL_WIDTH * '\u2500' + '\u252C') + CELL_WIDTH * '\u2500' + '\u2510\n'

    def space_lines(self):
        return GRID_SIZE * ('\u2502' + CELL_WIDTH * ' ') + '\u2502\n'

    def grid_lines(self):
        return '\u251C' + (GRID_SIZE - 1) * (CELL_WIDTH * '\u2500' + '\u253C') + CELL_WIDTH * '\u2500' + '\u2524\n'

    def bottom_lines(self):
        return '\u2514' + (GRID_SIZE - 1) * (CELL_WIDTH * '\u2500' + '\u2534') + CELL_WIDTH * '\u2500' + '\u2518\n'

    def row_str(self, row):
        """
        Returns a string representing a line of the grid containing numbers.
        """
        out = '\u2502'
        for i in range(GRID_SIZE):
            cell = self.spaces[row][i]
            if cell is None:
                cell = ' '
            else:
                cell = str(cell)
            lspaces = ' ' * math.ceil((CELL_WIDTH - len(cell)) / 2)
            rspaces = ' ' * math.floor((CELL_WIDTH - len(cell)) / 2)
            out += f"{lspaces}{cell}{rspaces}"
            out += '\u2502'
        out += '\n'
        return out

    def get_blank_spaces(self):
        blank_spaces = []
        for i in range(len(self.spaces)):
            for j in range(len(self.spaces)):
                if self.spaces[i][j] is None:
                    blank_spaces += [(i, j)]
        return blank_spaces

    def add_random_tile(self) -> None:
        """
        Adds a random tile to a blank space on the board.
        """
        selected_space = random.choice(self.get_blank_spaces())

        # set space to one of the 
        self.spaces[selected_space[0]][selected_space[1]] = random.choices([BASE_NUMBER, BASE_NUMBER * 2], weights=[0.9, 0.1])[0]

    def has_moves(self) -> bool:
        """
        Determines whether another move is possible.
        """
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.spaces[i][j] is None:
                    return True
                try:
                    if self.spaces[i][j] == self.spaces[i+1][j]:
                        return True
                except:
                    pass
                try:
                    if self.spaces[i][j] == self.spaces[i][j+1]:
                        return True
                except:
                    pass
        return False

    def horizontal_move(self, shift_func):
        """
        Attempts to move tiles horizontally according to the specified function. 
        Returns a boolean indicating whether any tiles were moved or combined.
        """
        changed = False
        for row in range(GRID_SIZE):
            self.spaces[row], is_changed, score_add = shift_func(self.spaces[row])
            if is_changed: changed = True
            self.score += score_add
        return changed

    
    def vertical_move(self, shift_func) -> bool:
        """
        Attempts to move tiles vertically according to the specified function. 
        Returns a boolean indicating whether any tiles were moved or combined.
        """
        changed = False
        for col in range(GRID_SIZE):
            column = [self.spaces[row][col] for row in range(GRID_SIZE)]
            new_column, is_changed, score_add = shift_func(column)
            for row in range(GRID_SIZE):
                self.spaces[row][col] = new_column[row]
            if is_changed: changed = True
            self.score += score_add
        return changed

    def left(self) -> bool:
        """
        Attempts to move tiles to the left. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        return self.horizontal_move(row_left)

    def right(self) -> bool:
        """
        Attempts to move tiles to the right. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        return self.horizontal_move(row_right)

    def up(self) -> bool:
        """
        Attempts to move tiles up. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        return self.vertical_move(row_left)

    def down(self) -> bool:
        """
        Attempts to move tiles down. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        return self.vertical_move(row_right)
    
    def make_move(self, direction) -> bool:
        """
        Given a direction, attempt to move the tiles in that direction. 
        Returns a boolean indicating whether any tiles were moved or combined.
        """
        return getattr(self, direction)()

    def is_legal_move(self, direction) -> bool:
        """
        Return whether moving in a given direction will have any effect.
        """
        return self.copy().make_move(direction)

    def get_legal_moves(self) -> list:
        """
        Return a list of legal move directions.
        """
        return [action for action in PLAYER_ACTIONS if self.is_legal_move(action)]

    def get_possible_successors(self) -> list:
        """
        Return a list of possible next game states.
        """
        successors = []
        for action in PLAYER_ACTIONS:
            copy = self.copy()
            if copy.make_move(action): successors.append(copy)
        return successors