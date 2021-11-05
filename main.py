import random
import math
import click

CELL_WIDTH = 7

class GameBoard():
    def __init__(self) -> None:
        self.score = 0
        self.spaces = [[None] * 4 for i in range(4)]
        self.add_random_tile()
        self.add_random_tile()

    def __repr__(self):
        out = '\u250C' + 3 * (CELL_WIDTH * '\u2500' + '\u252C') + CELL_WIDTH * '\u2500' + '\u2510\n'
        out += self.space_lines()
        out += self.row_str(0)
        out += self.space_lines()
        out += '\u251C' + 3 * (CELL_WIDTH * '\u2500' + '\u253C') + CELL_WIDTH * '\u2500' + '\u2524\n'
        out += self.space_lines()
        out += self.row_str(1)
        out += self.space_lines()
        out += '\u251C' + 3 * (CELL_WIDTH * '\u2500' + '\u253C') + CELL_WIDTH * '\u2500' + '\u2524\n'
        out += self.space_lines()
        out += self.row_str(2)
        out += self.space_lines()
        out += '\u251C' + 3 * (CELL_WIDTH * '\u2500' + '\u253C') + CELL_WIDTH * '\u2500' + '\u2524\n'
        out += self.space_lines()
        out += self.row_str(3)
        out += self.space_lines()
        out += '\u2514' + 3 * (CELL_WIDTH * '\u2500' + '\u2534') + CELL_WIDTH * '\u2500' + '\u2518\n'
        out += f"Score: {self.score}"
        return out
    
    def space_lines(self):
        return 4 * ('\u2502' + CELL_WIDTH * ' ') + '\u2502\n'

    def row_str(self, row):
        out = '\u2502'
        for i in range(4):
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
        blank_spaces = []
        for i in range(len(self.spaces)):
            for j in range(len(self.spaces)):
                if self.spaces[i][j] is None:
                    blank_spaces += [(i, j)]
        selected_space = random.choice(blank_spaces)
        self.spaces[selected_space[0]][selected_space[1]] = random.choices([2, 4], weights=[0.9, 0.1])[0]

    def has_moves(self) -> None:
        for i in range(4):
            for j in range(4):
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
        changed = False
        board_copy = [[None] * 4 for i in range(4)]
        for col in range(4):
            for row in range(4):
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
        for row in range(4):
            for col in range(4):
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
        for i in range(col+1, 4):
            if board_copy[row][i] is not None:
                return (board_copy[row][i], i)
        return None

    def right(self) -> bool:
        changed = False
        board_copy = [[None] * 4 for i in range(4)]
        for col in range(3, -1, -1):
            for row in range(4):
                if self.spaces[row][col] is None:
                    continue
                if col == 3:
                    board_copy[row][col] = self.spaces[row][col]
                    continue
                first_right = self.find_first_right(board_copy, row, col)
                if first_right is None:
                    changed = True
                    board_copy[row][3] = self.spaces[row][col]
                elif first_right[0] == self.spaces[row][col]:
                    changed = True
                    board_copy[row][first_right[1]] *= -2
                    self.score += self.spaces[row][col] * 2
                elif first_right[1] > col + 1:
                    changed = True
                    board_copy[row][first_right[1] - 1] = self.spaces[row][col]
                else:
                    board_copy[row][col] = self.spaces[row][col]
        for row in range(4):
            for col in range(4):
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
        changed = False
        board_copy = [[None] * 4 for i in range(4)]
        for row in range(4):
            for col in range(4):
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
        for row in range(4):
            for col in range(4):
                if board_copy[row][col] is None:
                    self.spaces[row][col] = None
                else:
                    self.spaces[row][col] = abs(board_copy[row][col])
        return changed

    def find_first_down(self, board_copy, row, col) -> tuple[int, int]:
        """
        Returns a tuple of the value of the first non-empty cell above the given one,
            and the row index of that cell.
            Returns None if no cell found.
        """
        for i in range(row+1, 4):
            if board_copy[i][col] is not None:
                return (board_copy[i][col], i)
        return None

    def down(self) -> bool:
        changed = False
        board_copy = [[None] * 4 for i in range(4)]
        for row in range(3, -1, -1):
            for col in range(4):
                if self.spaces[row][col] is None:
                    continue
                if row == 3:
                    board_copy[row][col] = self.spaces[row][col]
                    continue
                first_down = self.find_first_down(board_copy, row, col)
                if first_down is None:
                    changed = True
                    board_copy[3][col] = self.spaces[row][col]
                elif first_down[0] == self.spaces[row][col]:
                    changed = True
                    board_copy[first_down[1]][col] *= -2
                    self.score += self.spaces[row][col] * 2
                elif first_down[1] > row + 1:
                    changed = True
                    board_copy[first_down[1] - 1][col] = self.spaces[row][col]
                else:
                    board_copy[row][col] = self.spaces[row][col]
        for row in range(4):
            for col in range(4):
                if board_copy[row][col] is None:
                    self.spaces[row][col] = None
                else:
                    self.spaces[row][col] = abs(board_copy[row][col])
        return changed

def handle(c, board):
    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    click.echo()
    if c == '\x1b' or c == 'q':
        click.echo('Exiting...')
        return False
    elif c == '\x1b[A' or c == 'w':
        if board.up():
            board.add_random_tile()
    elif c == '\x1b[B' or c == 's':
        if board.down():
            board.add_random_tile()
    elif c == '\x1b[C' or c == 'd':
        if board.right():
            board.add_random_tile()
    elif c == '\x1b[D' or c == 'a':
        if board.left():
            board.add_random_tile()
    print(board)
    return True

def play_game():
    board = GameBoard()
    print(board)
    while board.has_moves():
        if not handle(click.getchar(), board):
            break
    print("Game over")

if __name__ == "__main__":
    play_game()