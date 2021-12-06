from GameAgent import GameAgent, play_n_times

class LeftDownAgent(GameAgent):
  def __init__(self) -> None:
    self.left = True

  def get_move(self, board):
    if self.left:
      self.left = False
      if board.is_legal_move("left"):
        return "left"
    if board.is_legal_move("down"):
      self.left = True
      return "down"
    if board.is_legal_move("left"):
      self.Left = False
      return "left"
    if board.is_legal_move("up"):
      self.left = False
      return "up"
    self.left = True
    return "right"

play_n_times(LeftDownAgent(), 1000)