import sys
import click
from GameAgent import GameAgent

class UserAgent(GameAgent):
    def get_move(self, board):
        key = click.getchar()

        # esc or q
        if key == '\x1b' or key == 'q':
            print('Exiting...')
            sys.exit(0)
        
        # up or w
        elif key == '\x1b[A' or key == 'w':
            return 'up'

        # down or s
        elif key == '\x1b[B' or key == 's':
            return 'down'

        # right or d
        elif key == '\x1b[C' or key == 'd':
            return 'right'

        # left or a
        elif key == '\x1b[D' or key == 'a':
            return 'left'
        
        return self.get_move(board)