#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser
import pdb

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])
    """
     new added functions
    """
    def isPartOver(self, boards):
        return self.deadTest(boards[0]) or self.deadTest(boards[1]) or self.deadTest(boards[2])
    def isEmpty(self,boards):
        for row in boards:
            for element in row:
                if element !=False:
                    return False
        else:
            return True

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        self.winAction = "stop"
    def getAction(self, gameState, gameRules):
        """
        first step strategy
        """
        if gameRules.isEmpty(gameState.boards) and gameState.boards[0][4]==False:
            gameRules.fingerprint = []
            gameRules.fingerprint.append(gameState.generateSuccessor("A4"))
            gameRules.preAction = "A4"
            return "A4"

        """
        get the previous step of my opponent by compare the new getted gamestate with my last gamestate
        """
        preGameState = gameRules.fingerprint.pop()
        preOpponentLocation= [chr(i + 65)+str(j) for i, x in enumerate(gameState.boards) for j, y in enumerate(x) if y != preGameState.boards[i][j]][0]
        
        """
        get the gamestate of which board is not died
        """
        states = [] 
        for x in range(3):
                if gameRules.deadTest(gameState.boards[x]) != True:
                     states.append(chr(x + 65) + "4")


        actions = gameState.getLegalActions(gameRules)
        """
        pruning!!! since the number of actions for each move is quite big, only when number of remaining legal action <= 12 will we use minimax agent 
        to search all legal actions within all three boards. Otherwise, we will try to kill boards as soon as possible without losing the game.
        """
        if len(actions) <=12:
            self.MaxValue(gameState,gameRules,None,0)
        
        if len(states) == 3:
            for action in actions:
                           if self.MinValue(gameState.generateSuccessor(action), gameRules, states[0], 7) == -99:
                               self.winAction = action
                               break
                           elif self.MinValue(gameState.generateSuccessor(action), gameRules, states[1], 7) == -99:
                               self.winAction = action
                               break
                           elif self.MinValue(gameState.generateSuccessor(action), gameRules, states[2], 7) == -99:
                               self.winAction = action
                               break
            else:
                if preOpponentLocation[0] != gameRules.preAction[0]:
                    for x in range(9):
                        if gameState.boards[2][x] != False:
                            break
                    else:
                        gameRules.fingerprint.append(gameState.generateSuccessor("C4"))
                        gameRules.preAction = "C4"
                        return "C4"
                if preOpponentLocation[0] == "C":
                    for x in range(9):
                        if gameState.boards[1][x] != False:
                            break
                    else:
                        gameRules.fingerprint.append(gameState.generateSuccessor("B4"))
                        gameRules.preAction = "B4"
                        return "B4"
                tmp = []
                for i,x in enumerate(gameState.boards[ord(preOpponentLocation[0])-65]):
                    if x == True:
                        tmp.append(i)
                if len(tmp)>=2:
                    for j in range(9):
                        if j % 3 != tmp[0] % 3 and j % 3 != tmp[1] % 3:
                            if j//3 !=tmp[0]//3 and j//3 !=tmp[1]//3:
                                self.winAction = preOpponentLocation[0]+str(j)
                                break
                else:
                        self.MaxValue(gameState, gameRules, preOpponentLocation, 0)                            

        elif len(states) == 1:
                    self.MaxValue(gameState, gameRules, states[0], 0)
        elif len(states)==2:
             for x in range(0,3):
                 for y in range(0,9):
                     if gameState.boards[x][y]!=False:
                         break
                 else:
                    self.winAction = chr(x + 65) + "4"
                    break
             else:
                    value1 = self.MaxValue(gameState, gameRules, states[0], 0)
                    # print("value1 is ->",value1)    
                    value2 = self.MaxValue(gameState, gameRules, states[1], 0)
                    # print("value2 is ->",value2)
                    if value1==-198 and value2==198:
                        # print("P and N")
                        for action in actions:
                           if self.MinValue(gameState.generateSuccessor(action), gameRules, states[1], 7)==-198:
                               self.winAction = action
                               break
                        else:
                            # print("P and N no kill")
                            tmp = []
                            for i, x in enumerate(gameState.boards[ord(states[1][0]) - 65]):
                                if x== True:
                                    tmp.append(i)
                            if len(tmp)>=2:
                                for j in range(9):
                                    if j % 3 != tmp[0] % 3 and j % 3 != tmp[1] % 3:
                                        if j//3 !=tmp[0]//3 and j//3 !=tmp[1]//3:
                                            self.winAction =preOpponentLocation[0]+str(j)
                                            break
                    if value1 ==198 and value2 == -198:
                        # print("P and N")
                        for action in actions:
                           if self.MinValue(gameState.generateSuccessor(action), gameRules, states[0], 7) == -198:
                               self.winAction = action
                               break
                        else:
                            # print("P and N no kill")
                            tmp = []
                            for i, x in enumerate(gameState.boards[ord(states[0][0]) - 65]):
                                if x == True:
                                    tmp.append(i)
                            if len(tmp)>=2:
                                for j in range(9):
                                    if j % 3 != tmp[0] % 3 and j % 3 != tmp[1] % 3:
                                        if j//3 !=tmp[0]//3 and j//3 !=tmp[1]//3:
                                            self.winAction = preOpponentLocation[0]+str(j)
                                            break
                    if value1 == -198 and value2 == -198:
                        # print("N and N")
                        for action in actions:
                           if self.MinValue(gameState.generateSuccessor(action), gameRules, states[0], 7) == -198:
                               self.winAction = action
                               break
                           elif self.MinValue(gameState.generateSuccessor(action), gameRules, states[1], 7) == -198:
                               self.winAction = action
                               break
                        else:
                            # print("N and N no kill")
                            tmp = []
                            for i, x in enumerate(gameState.boards[ord(states[1][0]) - 65]):
                                if x== True:
                                    tmp.append(i)
                            if len(tmp)>=2:
                                for j in range(9):
                                    if j % 3 != tmp[0] % 3 and j % 3 != tmp[1] % 3:
                                        if j//3 !=tmp[0]//3 and j//3 !=tmp[1]//3:
                                            self.winAction =preOpponentLocation[0]+str(j)
                                            break
                                            
                    if value1==198 and value2 ==198:
                        # print("P and P")                    
                        self.MaxValue(gameState, gameRules, preOpponentLocation, 0)
        gameRules.fingerprint.append(gameState.generateSuccessor(self.winAction))
        gameRules.preAction = self.winAction
        gameRules.preAction = self.winAction
        return self.winAction
    def MaxValue(self, gameState, gameRules, preOpponentLocation,depth):
           
            actions = gameState.getLegalActions(gameRules)
            if len(actions)==0:
                return self.evaluationFunc(gameState, gameRules)
            if preOpponentLocation !=None:
                if gameRules.deadTest(gameState.boards[ord(preOpponentLocation[0]) - 65]) or depth == 8:
                    return self.evaluationFunc(gameState,gameRules)
                value = -float("inf")
                for i,action in enumerate(actions):
                    if action[0] == preOpponentLocation[0]:
                        successorState = gameState.generateSuccessor(action)
                        value1 = self.MinValue(successorState, gameRules,preOpponentLocation,depth+1)
                        if value1> value:
                            value =  value1
                            if depth ==0:
                                self.winAction = action
                return value
            if preOpponentLocation ==None:
                if gameRules.isGameOver(gameState.boards) or depth == 8:
                    return self.evaluationFunc(gameState, gameRules)
                value = -float("inf")
                for i, action in enumerate(actions):
                    successorState = gameState.generateSuccessor(action)
                    value1 = self.MinValue(successorState, gameRules, preOpponentLocation, depth + 1)
                    if value1 > value:
                        value = value1
                        if depth == 0:
                            self.winAction = action
                return value

    def MinValue(self, gameState, gameRules, preOpponentLocation,depth):
            
            actions = gameState.getLegalActions(gameRules)
            if len(actions)==0:
                return -self.evaluationFunc(gameState, gameRules)
            if preOpponentLocation !=None:
                if gameRules.deadTest(gameState.boards[ord(preOpponentLocation[0]) - 65]) or depth == 8:
                    return -self.evaluationFunc(gameState, gameRules)
                value = float("inf")
                for i,action in enumerate(actions):
                    if action[0] == preOpponentLocation[0]:
                        successorState = gameState.generateSuccessor(action)
                        value1 = self.MaxValue(successorState, gameRules,preOpponentLocation,depth + 1)
                        if value1< value:
                            if depth == 0:
                                self.winAction = action
                            value = value1
                return value
            if preOpponentLocation == None:
                if gameRules.isGameOver(gameState.boards) or depth == 8:
                    return -self.evaluationFunc(gameState, gameRules)
                value = float("inf")
                for i,action in enumerate(actions):
                    successorState = gameState.generateSuccessor(action)
                    value1 = self.MaxValue(successorState, gameRules,preOpponentLocation,depth + 1)
                    if value1< value:
                        if depth == 0:
                                self.winAction = action
                        value = value1
                return value



    def evaluationFunc(self, gameState, gameRules):
        if gameRules.isGameOver(gameState.boards):
                return 999
        value = 0
        for i in range(3):
            if gameRules.deadTest(gameState.boards[i])==True:
                value += 99
        return value
        


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 10000

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = TicTacToeAgent1()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                pdb.set_trace()
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
