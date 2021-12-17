import random
import statistics
import math
from GameAgent import GameAgent, play_n_times, play_with_agent
from GameBoard import GRID_SIZE, PLAYER_ACTIONS, GameBoard
from PerfTimer import perf_timer

class QLearningAgent(GameAgent):
  def __init__(self, learning_rate, discount, epsilon) -> None:
    self.learning_rate = learning_rate
    self.discount = discount
    self.epsilon = epsilon
    self.q_vals = {}

  def get_move(self, board):
    legal_moves = board.get_legal_moves()
    best_action = None
    best_val = None
    for action in legal_moves:
      val = self.get_q(board, action)
      if best_action is None or val > best_val:
        best_action = action
        best_val = val
    return best_action

  def get_q(self, state, action):
    hashed_state = state.hash_board()
    if ((hashed_state, action) in self.q_vals):
      return self.q_vals[hashed_state, action]
    else:
      return 0

  def get_action(self, board):
    legal_moves = board.get_legal_moves()
    if random.random() < self.epsilon:
      return random.choice(legal_moves)
    else:
      return self.get_move(board)

  def update_q_vals(self, board, action, error):
    self.q_vals[board.hash_board(), action] = self.get_q(board, action) + self.learning_rate*error
  
  def train(self):
      board = GameBoard()
      while board.has_moves():
        # choose action
        action = self.get_action(board)

        # take action
        prev_board = board.copy()
        if board.make_move(action):
          board.add_random_tile()
        reward = board.score - prev_board.score
        next_state = board

        # compute td-error
        next_q = max([self.get_q(next_state, next_action) for next_action in PLAYER_ACTIONS])
        error = reward + self.discount*next_q - self.get_q(prev_board, action)

        # update q-values
        self.update_q_vals(prev_board, action, error)
      highestTile = max(map(max, board.spaces))
      return (board.score, highestTile)

  def train_n_times(self, episodes = 100):
    scores = []
    highestTiles = []
    for i in range(episodes):
      score, highestTile = self.train()
      scores.append(score)
      highestTiles.append(highestTile)
    avgScore = sum(scores) / len(scores)
    print("Average score after training for", episodes, "games:", avgScore)
    print("Highest tile attained after training:", max(highestTiles))
    print("Median highest tile after training:", statistics.median(highestTiles))      

class ApproximateQLearningAgent(QLearningAgent):
  def __init__(self, learning_rate, discount, epsilon) -> None:
    super().__init__(learning_rate, discount, epsilon)
    self.features = [blank_feature, highest_tile_feature, sum_tiles_feature, corner_tile_feature]
    self.weights = [0]*len(self.features)

  def get_q(self, state, action):
    total = 0
    for i, feature in enumerate(self.features):
      total += (self.weights[i] * feature(state, action))
    return total

  def update_q_vals(self, board, action, error):
    for i, feature in enumerate(self.features):
      self.weights[i] += self.learning_rate*error*feature(board, action)

  def train_n_times(self, episodes = 100):
    super().train_n_times(episodes)
    print('Feature weights:')
    for i, feature in enumerate(self.features):
      print(feature.__name__ + ':', self.weights[i])


def new_board(board, action):
  new_board = board.copy()
  new_board.make_move(action)
  return new_board

def score_feature(old_board, action):
  board = new_board(old_board, action)
  return board.score

def blank_feature(old_board, action):
  board = new_board(old_board, action)
  return len(board.get_blank_spaces())

def sum_tiles_feature(old_board, action):
  board = new_board(old_board, action)
  values = set()
  for row in range(GRID_SIZE):
      for col in range(GRID_SIZE):
          tile = board.spaces[row][col]
          if tile != None: values.add(math.log(tile, 2))
  return sum(values)

def highest_tile_feature(old_board, action):
  board = new_board(old_board, action)
  highestVal = 0
  for row in range(GRID_SIZE):
      for col in range(GRID_SIZE):
          tile = board.spaces[row][col]
          if tile != None: highestVal = max(highestVal, tile)
  return math.log(highestVal, 2)

def corner_tile_feature(old_board, action):
  board = new_board(old_board, action)
  highestVal = 0
  for row in range(GRID_SIZE):
      for col in range(GRID_SIZE):
          tile = board.spaces[row][col]
          if tile != None: highestVal = max(highestVal, tile)
  if highestVal in [board.spaces[0][0], board.spaces[GRID_SIZE-1][0], board.spaces[0][GRID_SIZE-1], board.spaces[GRID_SIZE-1][GRID_SIZE-1]]:
    return 30
  else:
    return -30

approx_agent = ApproximateQLearningAgent(0.0001, 0.9, 0.9)
approx_agent.train_n_times(1000)
play_n_times(approx_agent, 100)


# features = [(score_feature, 0), (blank_feature, 0), (highest_tile_feature, 0), (sum_tiles_feature, 0)]
# features = [(blank_feature, 0), (highest_tile_feature, 0), (sum_tiles_feature, 0), (corner_tile_feature, 0)]
# features = [(blank_feature, -9.523), (highest_tile_feature, 0.756), (sum_tiles_feature, 3.33)]

# def get_q_features(state, action):
#   total = 0
#   for feature, weight in features:
#     # print(weight, feature(state, action))
#     total += (weight * feature(state, action))
#   # print(total)
#   return total

# def get_action(board, epsilon = 0.2):
#   legal_moves = board.get_legal_moves()
#   if random.random() < epsilon:
#     return random.choice(legal_moves)
#   else:
#     best_action = None
#     for action in legal_moves:
#       val = get_q(board.hash_board(), action)
#       if best_action is not None:
#         best_val = get_q(board.hash_board(), best_action)
#       if best_action is None or val > best_val:
#         best_action = action
#     return best_action

# def get_action_features(board, epsilon = 0.2):
#   legal_moves = board.get_legal_moves()
#   if random.random() < epsilon:
#     return random.choice(legal_moves)
#   else:
#     best_action = None
#     for action in legal_moves:
#       val = get_q_features(board, action)
#       if best_action is not None:
#         best_val = get_q_features(board, best_action)
#       if best_action is None or val > best_val:
#         best_action = action
#     return best_action

# play_with_agent(ExpectimaxAgent(5))

# play_n_times(ExpectimaxAgent(5), 100, True)

# def train(show_board = True, mute = False, epsilon = 0.2):
#     """
#     Simulates gameplay with the given agent.
#     """
#     learning_rate = 0.01
#     discount = 0.9

#     board = GameBoard()
#     if show_board: print(board)
#     while board.has_moves():
#         action = get_action(board, epsilon)
#         state = board.hash_board()
#         prev_score = board.score
#         if board.make_move(action):
#             board.add_random_tile()
#         reward = board.score - prev_score
#         # if board.has_moves():
#         #   reward = 0
#         # else:
#         #   reward = board.score
#         next_state = board.hash_board()
#         next_q = max([get_q(next_state, next_action) for next_action in PLAYER_ACTIONS])
#         q_vals[state, action] = get_q(state, action) + learning_rate*(reward + discount*next_q - get_q(state, action))
#         if show_board: print(board)
#     highestTile = max(map(max, board.spaces))
#     if not mute: 
#         print("Score:", board.score)
#         # print("Game over\nScore:", board.score, "\nHighest Tile:", highestTile)
#     return (board.score, highestTile)

# def train_features(show_board = True, mute = False, epsilon = 0.2):
#     """
#     Simulates gameplay with the given agent.
#     """
#     learning_rate = 0.0001
#     discount = 0.9

#     board = GameBoard()
#     if show_board: print(board)
#     while board.has_moves():
#         # choose action
#         action = get_action_features(board, epsilon)

#         # take action
#         prev_score = board.score
#         state = board.copy()
#         if board.make_move(action):
#             board.add_random_tile()
#         reward = board.score - prev_score
#         # if board.has_moves():
#         #   reward = 0
#         # else:
#         #   reward = board.score#-1/(board.score+1)
#         next_state = board

#         # compute td-error
#         next_q = max([get_q_features(next_state, next_action) for next_action in PLAYER_ACTIONS])
#         # print(reward, discount, next_q, get_q_features(state, action))
#         error = reward + discount*next_q - get_q_features(state, action)
#         # if (type(error) == int or type(error) == float):
#         #   print(reward, discount*next_q, get_q_features(state, action))

#         # update weights
#         for index, (feature, weight) in enumerate(features):
#           # print(weight, learning_rate, error, feature(state, action))
#           # print('for feat', index, 'got', learning_rate, error, feature(state, action))
#           # print('to', weight + learning_rate*error*feature(state, action))
#           features[index] = (feature, weight + learning_rate*error*feature(state, action))
#         # print([f[1] for f in features])
          
#         if show_board: print(board)
#     highestTile = max(map(max, board.spaces))
#     if not mute: 
#         print("Score:", board.score)
#         # print("Game over\nScore:", board.score, "\nHighest Tile:", highestTile)
#     return (board.score, highestTile)

# def train_n_times(episodes = 100, verbose = False, epsilon = 0.2):
#     scores = []
#     highestTiles = []
#     for i in range(episodes):
#         score, highestTile = train_features(False, not verbose, epsilon)
#         scores.append(score)
#         highestTiles.append(highestTile)
#     avgScore = sum(scores) / len(scores)
#     print("Average score after", episodes, "games:", avgScore)
#     print("Highest tile attained:", max(highestTiles))
#     print("Median highest tile:", statistics.median(highestTiles))

# def print_features():
#   print([(feature.__name__, weight) for feature, weight in features])

# for i in range(40):
#   train_n_times(100, False, 0.7)
#   print_features()
# print('MOVING ON')
# for i in range(100):
#   train_n_times(100, False, 0)
#   print_features()
# train_n_times(1000, False, 0.4)
# train_n_times(1000, False, 0.1)
# train()
# print(q_vals)

# feature ideas: score, blank spaces, highest tile, sum of unique tiles
