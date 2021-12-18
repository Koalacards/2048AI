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

  def get_q(self, board, action):
    hashed_board = board.hash_board()
    if ((hashed_board, action) in self.q_vals):
      return self.q_vals[hashed_board, action]
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
        if reward > 0:
          reward = math.log(reward, 2)

        # compute td-error
        next_q = max([self.get_q(board, next_action) for next_action in PLAYER_ACTIONS])
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

  def get_q(self, board, action):
    total = 0
    for i, feature in enumerate(self.features):
      total += (self.weights[i] * feature(board, action))
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
play_n_times(approx_agent, 1000)