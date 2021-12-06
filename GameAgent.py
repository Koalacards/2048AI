from GameBoard import GameBoard

class GameAgent():
  def get_move(self, board):
    pass

def play_with_agent(agent, show_board = True, mute = False):
    """
    Simulates gameplay with the given agent.
    """
    board = GameBoard()
    if show_board: print(board)
    while board.has_moves():
        if board.make_move(agent.get_move(board)):
            board.add_random_tile()
        if show_board: print(board)
    if not mute: print("Game over\nScore:", board.score)
    return board.score

def play_n_times(agent, num_games = 100):
    scores = [play_with_agent(agent, False, True) for i in range(num_games)]
    avgScore = sum(scores) / len(scores)
    print("Average score after", num_games, "games:", avgScore)
    return avgScore