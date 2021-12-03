import copy
from GameAgent import GameAgent, PLAYER_ACTIONS, play_n_times, play_with_agent

class ExpectimaxState():
    def __init__(self, board, player_turn = True) -> None:
        self.board = board
        self.player_turn = player_turn

    def clone_board(self):
      return copy.deepcopy(self.board)

    def generate_successor(self, action):
      new_board = self.clone_board()
      if self.player_turn:
        getattr(new_board, action)()
      else:
        new_board.spaces[action[0]][action[1]] = action[2]
      return ExpectimaxState(new_board, not self.player_turn)

    def get_legal_actions(self):
      if self.player_turn:
        return [action for action in PLAYER_ACTIONS if getattr(self.clone_board(), action)()]
      else:
        moves = []
        for i in range(len(self.board.spaces)):
            for j in range(len(self.board.spaces)):
                if self.board.spaces[i][j] is None:
                    moves += [(i, j, 2)]
                    moves += [(i, j, 4)]
        return moves

    def get_score(self):
      return self.board.score

    def is_over(self):
      return not self.board.has_moves()


class ExpectimaxAgent(GameAgent):
  def __init__(self, max_depth = 3) -> None:
      self.max_depth = max_depth

  def evaluate(self, state):
      return state.get_score()

  def get_move(self, board):
      return self.get_action(ExpectimaxState(board))
  
  def get_next_action_values(self, state, turn):
      return [self.value(state.generate_successor(action), turn + 1) for action in state.get_legal_actions()]

  def max_value(self, state, turn):
      return max(self.get_next_action_values(state, turn))

  def avg_value(self, state, turn):
      next_action_values = self.get_next_action_values(state, turn)
      return sum(next_action_values) / len(next_action_values)

  def value(self, state, turn = 0):
      if state.is_over(): return state.get_score()
      if turn >= self.max_depth: return self.evaluate(state)
      if state.player_turn: return self.max_value(state, turn)
      else: return self.avg_value(state, turn)

  def get_action(self, game_state):
      best_action = None
      best_action_value = 0
      for action in game_state.get_legal_actions():
          action_value = self.value(game_state.generate_successor(action))
          if best_action == None or action_value > best_action_value:
              best_action = action
              best_action_value = action_value
      
      return best_action

# play_with_agent(ExpectimaxAgent(1))

play_n_times(ExpectimaxAgent(1), 10)