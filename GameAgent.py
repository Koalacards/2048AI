from GameBoard import GameBoard

PLAYER_ACTIONS = ['up', 'down', 'left', 'right']

class GameAgent():
  def get_move(self, board):
    pass

def make_move(move, board) -> None:
    moveFunc = getattr(board, move) # get move method from method name
    if moveFunc(): # make move
        board.add_random_tile()

def play_with_agent(agent, show_board = True, mute = False):
    """
    Simulates gameplay with the given agent.
    """
    board = GameBoard()
    if show_board: print(board)
    while board.has_moves():
        make_move(agent.get_move(board), board)
        if show_board: print(board)
    if not mute: print("Game over\nScore:", board.score)
    return board.score

def play_n_times(agent, num_games = 100):
    scores = [play_with_agent(agent, False, True) for i in range(num_games)]
    avgScore = sum(scores) / len(scores)
    print("Average score after", num_games, "games:", avgScore)
    return avgScore