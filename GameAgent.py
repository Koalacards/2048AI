import statistics
from GameBoard import GameBoard
from time import time

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
        ts = time()
        score, highestTile = play_with_agent(agent, False, True)
        if verbose:
            print(f"Completed game {i + 1}/{num_games}! Score: {score} Highest Tile: {highestTile}")
            print(f"Game completed in {time()-ts} seconds")
        scores.append(score)
        highestTiles.append(highestTile)
    avgScore = sum(scores) / len(scores)
    print("Average score after", num_games, "games:", avgScore)
    print("Highest tile attained:", max(highestTiles))
    print("Median highest tile:", statistics.median(highestTiles))
    _tile_distribution(highestTiles)

def _tile_distribution(highestTiles):
    total_tiles = len(highestTiles)
    tile_dict = {}
    for tile in highestTiles:
        if tile_dict.get(tile, None) is None:
            tile_dict[tile] = 1
        else:
            tile_dict[tile] = tile_dict[tile] + 1
    print("Highest Tile Percentages:")
    for key, value in sorted(tile_dict.items()):
        percent = (value / total_tiles) * 100
        print(f"{key}: {percent}%")
    