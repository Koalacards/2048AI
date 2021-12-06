import random
from GameAgent import GameAgent, play_n_times

class RandomAgent(GameAgent):
  def get_move(self, board):
    return random.choice(board.get_legal_moves())

play_n_times(RandomAgent(), 1000)