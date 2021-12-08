from GameAgent import GameAgent, play_n_times, play_with_agent
from GameBoard import GRID_SIZE
from PerfTimer import perf_timer

class ExpectimaxState():
    def __init__(self, board, player_turn = True) -> None:
        self.board = board
        self.player_turn = player_turn

    def generate_successor(self, action):
      """
      Returns state obtained by taking the given action.
      """
      new_board = self.board.copy()
      if self.player_turn:
        new_board.make_move(action)
      else:
        new_board.spaces[action[0]][action[1]] = action[2]
      return ExpectimaxState(new_board, not self.player_turn)

    def get_legal_actions(self, tile = 2):
      if self.player_turn:
        return self.board.get_legal_moves()
      else:
        moves = []
        for i in range(len(self.board.spaces)):
            for j in range(len(self.board.spaces)):
                if self.board.spaces[i][j] is None:
                    moves += [(i, j, tile)]
        return moves

    def get_score(self):
      return self.board.score

    def is_over(self):
      return not self.board.has_moves()


class ExpectimaxAgent(GameAgent):
  def __init__(self, max_depth = 3) -> None:
      self.max_depth = max_depth
  
  def get_terminal_value(self, state):
      return state.get_score()

  def evaluate(self, state):
      return state.get_score()

  def max_value(self, state, depth):
      """
      Computes max value for player turn.
      """
      successors = [ExpectimaxState(board, not state.player_turn) for board in state.board.get_possible_successors()]
      return max([self.value(successor, depth + 1) for successor in successors])

  def avg_for_tile(self, state, depth, val):
      """
      Computes the average value for the adversary placing a tile of the given value.
      """
      vals = [self.value(state.generate_successor(action), depth + 1) for action in state.get_legal_actions(val)]
      return sum(vals) / len(vals)

  def avg_value(self, state, depth):
      """
      Compute weighted average value for adversary turn.
      """
      avg_for_2 = self.avg_for_tile(state, depth, 2)
      avg_for_4 = self.avg_for_tile(state, depth, 4)
      return 0.9*avg_for_2 + 0.1*avg_for_4

  def value(self, state, depth = 1):
      """
      Computes the value of the state.
      """
      if state.is_over(): return self.get_terminal_value(state)
      if depth >= self.max_depth: return self.evaluate(state)
      if state.player_turn: return self.max_value(state, depth)
      else: return self.avg_value(state, depth)

  def get_action(self, game_state):
      best_action = None
      best_action_value = 0
      for action in game_state.get_legal_actions():
          action_value = self.value(game_state.generate_successor(action))
          if best_action == None or action_value > best_action_value:
              best_action = action
              best_action_value = action_value
      return best_action

class SmarterExpectimaxAgent(ExpectimaxAgent):
    """
    WIP
    """
    def get_terminal_value(self, state):
        # return 0
        # highest tile
        highestVal = 0
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile = state.board.spaces[row][col]
                if tile != None: highestVal = max(highestVal, tile)
        return highestVal

    def evaluate(self, state):
        # tile sum
        values = set()
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile = state.board.spaces[row][col]
                if tile != None: values.add(tile)
        tile_sum = sum(values)
        score = state.get_score()
        return self.get_terminal_value(state) * 1000 + score

play_with_agent(ExpectimaxAgent(5))

# play_n_times(ExpectimaxAgent(2), 10)