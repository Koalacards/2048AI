import copy
from GameAgent import GameAgent, PLAYER_ACTIONS, play_n_times, play_with_agent

class ExpectimaxState():
    def __init__(self, board, playerTurn = True) -> None:
        self.board = board
        self.playerTurn = playerTurn

    def cloneBoard(self):
      return copy.deepcopy(self.board)

    def generateSuccessor(self, action):
      newBoard = self.cloneBoard()
      if self.playerTurn:
        getattr(newBoard, action)()
      else:
        newBoard.spaces[action[0]][action[1]] = action[2]
      return ExpectimaxState(newBoard, not self.playerTurn)

    def getLegalActions(self):
      if self.playerTurn:
        return [action for action in PLAYER_ACTIONS if getattr(self.cloneBoard(), action)()]
      else:
        moves = []
        for i in range(len(self.board.spaces)):
            for j in range(len(self.board.spaces)):
                if self.board.spaces[i][j] is None:
                    moves += [(i, j, 2)]
                    moves += [(i, j, 4)]
        return moves

    def getScore(self):
      return self.board.score

    def isOver(self):
      return not self.board.has_moves()


class ExpectimaxAgent(GameAgent):
  def __init__(self, max_depth = 3) -> None:
      self.max_depth = max_depth

  def evaluate(self, state):
      return state.getScore()

  def get_move(self, board):
      return self.getAction(ExpectimaxState(board))
  
  def getNextActionValues(self, state, turn):
      return [self.value(state.generateSuccessor(action), turn + 1) for action in state.getLegalActions()]

  def maxValue(self, state, turn):
      return max(self.getNextActionValues(state, turn))

  def avgValue(self, state, turn):
      nextActionValues = self.getNextActionValues(state, turn)
      return sum(nextActionValues) / len(nextActionValues)

  def value(self, state, turn = 0):
      if state.isOver(): return state.getScore()
      if turn >= self.max_depth: return self.evaluate(state)
      if state.playerTurn: return self.maxValue(state, turn)
      else: return self.avgValue(state, turn)

  def getAction(self, gameState):
      bestAction = None
      bestActionValue = 0
      for action in gameState.getLegalActions():
          actionValue = self.value(gameState.generateSuccessor(action))
          if bestAction == None or actionValue > bestActionValue:
              bestAction = action
              bestActionValue = actionValue
      
      return bestAction

# play_with_agent(ExpectimaxAgent(1))

play_n_times(ExpectimaxAgent(1), 10)