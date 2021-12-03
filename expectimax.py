import copy
from main import GameBoard, handle

depth = 3

playerActions = ['up', 'down', 'left', 'right']

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
        return [action for action in playerActions if getattr(self.cloneBoard(), action)()]
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


def getNextActionValues(state, turn):
    return [value(state.generateSuccessor(action), turn + 1) for action in state.getLegalActions()]

def maxValue(state, turn):
    return max(getNextActionValues(state, turn))

def avgValue(state, turn):
    nextActionValues = getNextActionValues(state, turn)
    return sum(nextActionValues) / len(nextActionValues)

def value(state, turn = 0):
    if state.isOver() or turn >= depth: return state.getScore()
    if state.playerTurn: return maxValue(state, turn)
    else: return avgValue(state, turn)

def getAction(gameState):
    bestAction = None
    bestActionValue = 0
    for action in gameState.getLegalActions():
        actionValue = value(gameState.generateSuccessor(action))
        if bestAction == None or actionValue > bestActionValue:
            bestAction = action
            bestActionValue = actionValue
    
    return bestAction

actionMap = {
  'up': 'w',
  'down': 's',
  'left': 'a',
  'right': 'd'
}

def play_game_bot():
    board = GameBoard()
    print(board)
    while board.has_moves():
        state = ExpectimaxState(board)
        bestAction = getAction(state)
        handle(actionMap[bestAction], board)
    print("Game over")

play_game_bot()