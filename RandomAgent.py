import random
from GameAgent import PLAYER_ACTIONS, GameAgent, play_n_times, play_with_agent

class RandomAgent(GameAgent):
  def get_move(self, board):
    return random.choice(PLAYER_ACTIONS)

play_n_times(RandomAgent(), 1000)