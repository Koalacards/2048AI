import random
from GameAgent import GameAgent, play_n_times

# Agent that moves in a set direction each turn, when possible.
class SingleDirectionAgent(GameAgent):
  def get_move(self, board):
    if board.is_legal_move("down"):
      return "down"
    else:
      return random.choice(board.get_legal_moves())
      

play_n_times(SingleDirectionAgent(), 1000)