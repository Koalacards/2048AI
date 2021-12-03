from GameBoard import GameBoard

PLAYER_ACTIONS = ['up', 'down', 'left', 'right']

class GameAgent():
  def get_move(self, board):
    pass

def make_move(move, board) -> None:
    moveFunc = getattr(board, move) # get move method from method name
    if moveFunc(): # make move
        board.add_random_tile()

def play_with_agent(agent, show_board = True):
    """
    Simulates gameplay with the given agent
    """
    board = GameBoard()
    if show_board: print(board)
    while board.has_moves():
        make_move(agent.get_move(board), board)
        if show_board: print(board)
    print("Game over")
    print("Score:", board.score)