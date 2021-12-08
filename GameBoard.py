import random
import math

CELL_WIDTH = 7
CELL_HEIGHT = 3
BASE_NUMBER = 2
GRID_SIZE = 4
PLAYER_ACTIONS = ['up', 'down', 'left', 'right']

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
            for j in range(len(self.spaces)):
                new_board.spaces[i][j] = self.spaces[i][j]
        return new_board

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

    def add_random_tile(self) -> None:
        """
        Adds a random tile to a blank space on the board.
        """
        blank_spaces = []
        for i in range(len(self.spaces)):
            for j in range(len(self.spaces)):
                if self.spaces[i][j] is None:
                    blank_spaces += [(i, j)]
        selected_space = random.choice(blank_spaces)

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

    def find_first_left(self, board_copy, row, col) -> tuple[int, int]:
        """
        Returns a tuple of the value of the first non-empty cell to the left of the given one,
            and the column index of that cell.
            Returns None if no cell found.
        """
        for i in range(col-1, -1, -1):
            if board_copy[row][i] is not None:
                return (board_copy[row][i], i)
        return None

    def left(self) -> bool:
        """
        Attempts to move tiles to the left. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        changed = False
        board_copy = [[None] * GRID_SIZE for i in range(GRID_SIZE)]
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE):
                if self.spaces[row][col] is None:
                    continue
                if col == 0:
                    board_copy[row][col] = self.spaces[row][col]
                    continue
                first_left = self.find_first_left(board_copy, row, col)
                if first_left is None:
                    changed = True
                    board_copy[row][0] = self.spaces[row][col]
                elif first_left[0] == self.spaces[row][col]:
                    changed = True
                    board_copy[row][first_left[1]] *= -2
                    self.score += self.spaces[row][col] * 2
                elif first_left[1] < col - 1:
                    changed = True
                    board_copy[row][first_left[1] + 1] = self.spaces[row][col]
                else:
                    board_copy[row][col] = self.spaces[row][col]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board_copy[row][col] is None:
                    self.spaces[row][col] = None
                else:
                    self.spaces[row][col] = abs(board_copy[row][col])
        return changed

    def find_first_right(self, board_copy, row, col) -> tuple[int, int]:
        """
        Returns a tuple of the value of the first non-empty cell to the right of the given one,
            and the column index of that cell.
            Returns None if no cell found.
        """
        for i in range(col+1, GRID_SIZE):
            if board_copy[row][i] is not None:
                return (board_copy[row][i], i)
        return None

    def right(self) -> bool:
        """
        Attempts to move tiles to the right. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        changed = False
        board_copy = [[None] * GRID_SIZE for i in range(GRID_SIZE)]
        for col in range(GRID_SIZE - 1, -1, -1):
            for row in range(GRID_SIZE):
                if self.spaces[row][col] is None:
                    continue
                if col == GRID_SIZE - 1:
                    board_copy[row][col] = self.spaces[row][col]
                    continue
                first_right = self.find_first_right(board_copy, row, col)
                if first_right is None:
                    changed = True
                    board_copy[row][GRID_SIZE - 1] = self.spaces[row][col]
                elif first_right[0] == self.spaces[row][col]:
                    changed = True
                    board_copy[row][first_right[1]] *= -2
                    self.score += self.spaces[row][col] * 2
                elif first_right[1] > col + 1:
                    changed = True
                    board_copy[row][first_right[1] - 1] = self.spaces[row][col]
                else:
                    board_copy[row][col] = self.spaces[row][col]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board_copy[row][col] is None:
                    self.spaces[row][col] = None
                else:
                    self.spaces[row][col] = abs(board_copy[row][col])
        return changed

    def find_first_up(self, board_copy, row, col) -> tuple[int, int]:
        """
        Returns a tuple of the value of the first non-empty cell above the given one,
            and the row index of that cell.
            Returns None if no cell found.
        """
        for i in range(row-1, -1, -1):
            if board_copy[i][col] is not None:
                return (board_copy[i][col], i)
        return None

    def up(self) -> bool:
        """
        Attempts to move tiles up. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        changed = False
        board_copy = [[None] * GRID_SIZE for i in range(GRID_SIZE)]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.spaces[row][col] is None:
                    continue
                if row == 0:
                    board_copy[row][col] = self.spaces[row][col]
                    continue
                first_up = self.find_first_up(board_copy, row, col)
                if first_up is None:
                    changed = True
                    board_copy[0][col] = self.spaces[row][col]
                elif first_up[0] == self.spaces[row][col]:
                    changed = True
                    board_copy[first_up[1]][col] *= -2
                    self.score += self.spaces[row][col] * 2
                elif first_up[1] < row - 1:
                    changed = True
                    board_copy[first_up[1] + 1][col] = self.spaces[row][col]
                else:
                    board_copy[row][col] = self.spaces[row][col]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board_copy[row][col] is None:
                    self.spaces[row][col] = None
                else:
                    self.spaces[row][col] = abs(board_copy[row][col])
        return changed

    def find_first_down(self, board_copy, row, col) -> tuple[int, int]:
        """
        Returns a tuple of the value of the first non-empty cell below the given one,
            and the row index of that cell.
            Returns None if no cell found.
        """
        for i in range(row+1, GRID_SIZE):
            if board_copy[i][col] is not None:
                return (board_copy[i][col], i)
        return None

    def down(self) -> bool:
        """
        Attempts to move tiles down. Returns a boolean indicating whether
        any tiles were moved or combined.
        """
        changed = False
        board_copy = [[None] * GRID_SIZE for i in range(GRID_SIZE)]
        
        # iterate through rows in reverse order
        for row in range(GRID_SIZE - 1, -1, -1):
            for col in range(GRID_SIZE):
                # this cell is blank
                if self.spaces[row][col] is None:
                    continue

                # this cell is in the bottom row
                if row == GRID_SIZE - 1:
                    board_copy[row][col] = self.spaces[row][col]
                    continue

                # find first non-empty cell below this one
                first_down = self.find_first_down(board_copy, row, col)

                # all cells below are empty
                if first_down is None:
                    changed = True
                    board_copy[GRID_SIZE - 1][col] = self.spaces[row][col]
                
                # this cell matches the cell below
                elif first_down[0] == self.spaces[row][col]:
                    changed = True
                    board_copy[first_down[1]][col] *= -2
                    self.score += self.spaces[row][col] * 2

                # the cell below is empty
                elif first_down[1] > row + 1:
                    changed = True
                    board_copy[first_down[1] - 1][col] = self.spaces[row][col]
                
                # the cell below is adjacent and does not match
                else:
                    board_copy[row][col] = self.spaces[row][col]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board_copy[row][col] is None:
                    self.spaces[row][col] = None
                else:
                    self.spaces[row][col] = abs(board_copy[row][col])
        return changed
    
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