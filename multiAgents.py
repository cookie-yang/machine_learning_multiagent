from util import manhattanDistance
from game import Directions
import random, util
import pdb

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        para1 = min([manhattanDistance(x, newPos) for x in prevFood.asList(True)])
        para2 = min([manhattanDistance(newPos, x.getPosition())
                     for x in newGhostStates])
        if para2 <= 1:
          return 0
        if para1 ==0:
          return float("inf")
        if para2>=7:
          return 1.0/para1
        if para2<=4:
          return 0.72*para2+3.0/para1
        else:
          return 6/para1+0.5*para2
        return successorGameState.getScore()
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        depth = self.depth 
        return max([(self.MinValue(gameState.generateSuccessor(
            0, action), 1, depth, numAgents),action) for action in gameState.getLegalActions()])[1]

    def MaxValue(self, gameState, depth, numAgents):
      if gameState.isWin == True or gameState.isLose == True or depth ==0:
        return self.evaluationFunction(gameState)
      else:
        successorGameState=[gameState.generateSuccessor(0, action) for action in gameState.getLegalActions(0)]
        if len(successorGameState)==0:
          return self.evaluationFunction(gameState)
        return max([self.MinValue(gameState, 1, depth, numAgents) for gameState in successorGameState])


    def MinValue(self, gameState, agentIndex, depth, numAgents):
      if gameState.isWin == True or gameState.isLose == True or depth == 0:
        return self.evaluationFunction(gameState)
      successorGameState = [gameState.generateSuccessor(agentIndex, action) for action in gameState.getLegalActions(agentIndex)]
      if agentIndex == numAgents-1:
         if len(successorGameState) == 0:
          return self.evaluationFunction(gameState)
         return min([self.MaxValue(gameState, depth - 1, numAgents) for gameState in successorGameState])
      else:
        if len(successorGameState) == 0:
          return self.evaluationFunction(gameState)
        return min([self.MinValue(gameState, agentIndex + 1, depth, numAgents) for gameState in successorGameState])

        






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.actionList = []
        depth = self.depth
        numAgents  = gameState.getNumAgents()
        # pdb.set_trace()
        value = self.MaxValue(gameState,-float("inf"),float("inf"),depth,numAgents)
        for x in self.actionList:
          if x[0]==value:
            return x[1]

    def MaxValue(self,gameState,maxV,minV,depth,numAgents):
      if gameState.isWin == True or gameState.isLose == True or depth == 0:
        return self.evaluationFunction(gameState)
      if len(gameState.getLegalActions(0)) == 0:
        return self.evaluationFunction(gameState)
      value = -float("inf")
      for action in gameState.getLegalActions(0):
        successorGameState = (gameState.generateSuccessor(0,action),action)
        value1 = self.MinValue(successorGameState[0],1,maxV,minV,depth,numAgents)
        value = max(value,value1)
        if depth ==self.depth:
          self.actionList.append((value1,action))
        if value > minV:
          return value
        maxV = max(value,maxV)
      return value

    def MinValue(self, gameState, agentIndex, maxV, minV, depth, numAgents):
      if gameState.isWin == True or gameState.isLose == True or depth == 0:
        return self.evaluationFunction(gameState)
      if len(gameState.getLegalActions(agentIndex)) == 0:
        return self.evaluationFunction(gameState)
      if agentIndex == numAgents - 1:
        value = float("inf")
        for action in gameState.getLegalActions(agentIndex):
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          value = min(value,self.MaxValue(successorGameState,maxV,minV,depth-1,numAgents))
          if value < maxV:
            return value
          minV = min(value,minV)
        return value
      else:
        value = float("inf")
        for action in gameState.getLegalActions(agentIndex):
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          value = min(value,self.MinValue(successorGameState,agentIndex+1,maxV,minV,depth,numAgents))
          if value < maxV:
            return value
          minV = min(value,minV)
        return value
        


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        depth = self.depth
        numAgents = gameState.getNumAgents()
        # pdb.set_trace()
        self.MaxValue(gameState,depth,numAgents)
        return self.action
       
    def MaxValue(self, gameState,depth, numAgents):
      if gameState.isWin == True or gameState.isLose == True or depth == 0:
        return self.evaluationFunction(gameState) 
      if len(gameState.getLegalActions(0)) == 0:
        return self.evaluationFunction(gameState)
      value1 = [(self.ChanceValue(gameState.generateSuccessor(0, action), 1,depth, numAgents),action) for action in gameState.getLegalActions(0)]
      value = max(value1)
      if depth == self.depth:
          self.action = value[1]
      return value[0]

    def ChanceValue(self, gameState, agentIndex, depth, numAgents):
      if gameState.isWin == True or gameState.isLose == True or depth == 0:
        return self.evaluationFunction(gameState) 
      if len(gameState.getLegalActions(agentIndex)) == 0:
        return self.evaluationFunction(gameState)
      if agentIndex == numAgents - 1:
        valueList1 = [(self.MaxValue(gameState.generateSuccessor(agentIndex, action),depth - 1, numAgents),action) for action in gameState.getLegalActions(agentIndex)]
        valueList = [x[0]for x in valueList1]
        return sum(valueList) / len(valueList)
      else:
        valueList = [self.ChanceValue(gameState.generateSuccessor(agentIndex, action), agentIndex+1,depth, numAgents) for action in gameState.getLegalActions(agentIndex)]
        return sum(valueList)/len(valueList)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      <In this evaluation function, reciprocal of distance between pacman and nearest food, reciprocal of number of remaining food, reciprocal  of distance from pacman to all remaining food, score of game as living penalty, distance between nearest ghost, reciprocal of number of capsules are taken into account with corresponding weights. When capsule is eaten and minimum ghost time is larger than the distance between pacman and nearest ghost, distance from nearest ghost will be replaced by reciprocal of distance with a high weight. >

    """
    "*** YOUR CODE HERE ***"
    pacPos = currentGameState.getPacmanPosition()
    preFood = currentGameState.getFood().asList(True)
    NumFood = currentGameState.getNumFood()
    GhostStates = currentGameState.getGhostStates()
    numCapsules = len(currentGameState.getCapsules())
    if currentGameState.isWin():
      return 99999+10 * currentGameState.getScore()
    if currentGameState.isLose():
          return -99999 + 10 * currentGameState.getScore()
    foodPara2 = sum([manhattanDistance(x, pacPos)for x in preFood])
    foodPara = min([(manhattanDistance(x, pacPos), x) for x in preFood])[0]
    ghostPara = min([manhattanDistance(pacPos, x.getPosition())for x in GhostStates])
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    if min(ScaredTimes) >= ghostPara:
      return (10 / foodPara + 1000 / NumFood + 100 / foodPara2 + 100 * currentGameState.getScore() + 5000 / ghostPara + 2000 / (numCapsules + 2))

    return (10 / foodPara + 1000 / NumFood + 100 / foodPara2 +100 * currentGameState.getScore() + 0.5*ghostPara + 2000 / (numCapsules+2))
   
    

# Abbreviation
better = betterEvaluationFunction

