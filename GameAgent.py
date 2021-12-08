import statistics
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
    highestTile = max(map(max, board.spaces))
    if not mute: 
        print("Game over\nScore:", board.score, "\nHighest Tile:", highestTile)
    return (board.score, highestTile)

def play_n_times(agent, num_games = 100, verbose = False):
    scores = []
    highestTiles = []
    for i in range(num_games):
        score, highestTile = play_with_agent(agent, False, not verbose)
        scores.append(score)
        highestTiles.append(highestTile)
    avgScore = sum(scores) / len(scores)
    print("Average score after", num_games, "games:", avgScore)
    print("Highest tile attained:", max(highestTiles))
    print("Median highest tile:", statistics.median(highestTiles))