import random
import statistics
from GameAgent import GameAgent, play_n_times, play_with_agent
from GameBoard import GRID_SIZE, PLAYER_ACTIONS, GameBoard
from PerfTimer import perf_timer

q_vals = {}

def get_q(state, action):
  if ((state, action) in q_vals):
    return q_vals[state, action]
  else:
    return 0

# class QLearningState():
#     def __init__(self, board) -> None:
#         self.board = board

#     def generate_successor(self, action):
#         """
#         Returns state obtained by taking the given action.
#         """
#         new_board = self.board.copy()
#         if new_board.make_move(action):
#             new_board.add_random_tile()
#         return QLearningState(new_board)

#     def get_legal_actions(self, tile = 2):
#         return self.board.get_legal_moves()

#     def get_score(self):
#         return self.board.score

#     def is_over(self):
#         return not self.board.has_moves()


# class QLearningAgent(GameAgent):
#     def __init__(self, learning_rate = 0.01, discount = 0.9, epsilon = 0.2) -> None:
#         self.learning_rate = learning_rate
#         self.discount = discount
#         self.epsilon = epsilon

#     def get_terminal_value(self, state):
#         return state.get_score()
        
#     def get_move(self, board):
#         return self.get_action(QLearningState(board))

#     def get_action(self, game_state):
#       pass

def get_action(board, epsilon = 0.2):
  legal_moves = board.get_legal_moves()
  if random.random() < epsilon:
    return random.choice(legal_moves)
  else:
    best_action = None
    for action in legal_moves:
      val = get_q(board.hash_board(), action)
      if best_action is not None:
        best_val = get_q(board.hash_board(), best_action)
      if best_action is None or val > best_val:
        best_action = action
    return best_action

# play_with_agent(ExpectimaxAgent(5))

# play_n_times(ExpectimaxAgent(5), 100, True)

def train(show_board = True, mute = False, epsilon = 0.2):
    """
    Simulates gameplay with the given agent.
    """
    learning_rate = 0.01
    discount = 0.9

    board = GameBoard()
    if show_board: print(board)
    while board.has_moves():
        action = get_action(board, epsilon)
        state = board.hash_board()
        prev_score = board.score
        if board.make_move(action):
            board.add_random_tile()
        reward = board.score - prev_score
        next_state = board.hash_board()
        next_q = max([get_q(next_state, next_action) for next_action in PLAYER_ACTIONS])
        q_vals[state, action] = get_q(state, action) + learning_rate*(reward + discount*next_q - get_q(state, action))
        if show_board: print(board)
    highestTile = max(map(max, board.spaces))
    if not mute: 
        print("Score:", board.score)
        # print("Game over\nScore:", board.score, "\nHighest Tile:", highestTile)
    return (board.score, highestTile)

def train_n_times(episodes = 100, verbose = False, epsilon = 0.2):
    scores = []
    highestTiles = []
    for i in range(episodes):
        score, highestTile = train(False, not verbose, epsilon)
        scores.append(score)
        highestTiles.append(highestTile)
    avgScore = sum(scores) / len(scores)
    print("Average score after", episodes, "games:", avgScore)
    print("Highest tile attained:", max(highestTiles))
    print("Median highest tile:", statistics.median(highestTiles))

train_n_times(5000, False, 0.9)
train_n_times(1000, False, 0.4)
train_n_times(1000, False, 0.1)
# train()
print(q_vals)