from util import manhattanDistance
from game import Directions
import random
import util
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min(
            [manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food)
                                  for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(
            newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(
            newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
            In part 1, I use a recursion function called "value" to implement 
        minimax search. When entering this function, first, we check whether it is 
        the end of a depth and change the agent to the next one who will pick 
        the max/min value from its leaf nodes.
            And then, check whether the currenGameState is terminal state or 
        acheives self.depth. If it is, return the self.evaluationFunction value
        of the state; If not, get the max(pacman)/min(ghost) value from recursing 
        this function with all the NextState which derived from the legalMoves of 
        currentGameState.
            Finally, return the optimal chose value and action which will lead 
        to the next state.
        """
        def value(currentGameState, now_depth, agentIndex):
            if agentIndex == currentGameState.getNumAgents() - 1:
                now_depth += 1
                agentIndex = 0
            else:
                agentIndex += 1

            if currentGameState.isWin() or currentGameState.isLose() or now_depth > self.depth:
                return self.evaluationFunction(currentGameState), 0

            legalMoves = currentGameState.getLegalActions(agentIndex)
            NextState = [currentGameState.getNextState(
                agentIndex, action) for action in legalMoves]
            stateValue = [value(nextState, now_depth, agentIndex)[0]
                          for nextState in NextState]

            if agentIndex == 0:
                v = max(stateValue)
            else:
                v = min(stateValue)

            val_indice = [index for index in range(
                len(stateValue)) if stateValue[index] == v]
            chosenIndex = random.choice(val_indice)

            return v, legalMoves[chosenIndex]

        (v, action) = value(gameState, 1, -1)
        return action
        raise NotImplementedError("To be implemented")
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
            In part 2, I use same recursive method which is roughly like part 1.
        The thing different is that I moved the "max_value" and "min_value" out 
        of the "value" function and add alpha and beta parameters into each 
        function to implement alpha-beta pruning.
            When entering "max_value" function, initialize v to negative infinite.
        Then, get the nextStateValue of one of the legal actions, if it larger than 
        v, update val with it. If v larger than beta, return (v, action) immediately 
        to prune the leaf nodes. Otherwise, keep getting other values and repeat 
        steps above. At last, return (v, action).
            Similarly, "min_value" is alike to "max_value", the thing needed to do 
        is alpha, beta exchanged and '>', '<' reversed.
        """
        def value(currentGameState, now_depth, agentIndex, alpha, beta):
            if agentIndex == currentGameState.getNumAgents() - 1:
                now_depth += 1
                agentIndex = 0
            else:
                agentIndex += 1

            if currentGameState.isWin() or currentGameState.isLose() or now_depth > self.depth:
                return self.evaluationFunction(currentGameState), 0
            if agentIndex == 0:
                return max_value(currentGameState, now_depth, agentIndex, alpha, beta)
            else:
                return min_value(currentGameState, now_depth, agentIndex, alpha, beta)

        def max_value(currentGameState, now_depth, agentIndex, alpha, beta):
            v = float('-inf')
            legalMoves = currentGameState.getLegalActions(agentIndex)

            for index in range(len(legalMoves)):
                nextStateValue = value(currentGameState.getNextState(
                    agentIndex, legalMoves[index]), now_depth, agentIndex, alpha, beta)[0]

                if v < nextStateValue:
                    chosenIndex = index
                    v = nextStateValue

                if v > beta:
                    return v, legalMoves[index]
                alpha = max(alpha, v)

            return v, legalMoves[chosenIndex]

        def min_value(currentGameState, now_depth, agentIndex, alpha, beta):
            v = float('inf')
            legalMoves = currentGameState.getLegalActions(agentIndex)

            for index in range(len(legalMoves)):
                nextStateValue = value(currentGameState.getNextState(
                    agentIndex, legalMoves[index]), now_depth, agentIndex, alpha, beta)[0]

                if v > nextStateValue:
                    chosenIndex = index
                    v = nextStateValue

                if v < alpha:
                    return v, legalMoves[index]
                beta = min(beta, v)

            return v, legalMoves[chosenIndex]

        alpha = float('-inf')
        beta = float('inf')
        (v, action) = value(gameState, 1, -1, alpha, beta)
        return action
        raise NotImplementedError("To be implemented")
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
            In part 3, I use the same recursive method which is roughly like part 1.
        The thing different is that I moved the "max_value" and "expected_value"
        out of the "value" function to implement expectimax search. 
            The "expected_value" function returns the expected value of a random-
        moving ghost. In this function, after evaluating all the values of NextState, 
        we calculate its expected value as v by: sum(NextStateValue)/len(legalMoves).
        And then randomly choose a action from legalMoves. Last, return (v, action).
        """
        def value(currentGameState, now_depth, agentIndex):
            if agentIndex == currentGameState.getNumAgents() - 1:
                now_depth += 1
                agentIndex = 0
            else:
                agentIndex += 1

            if currentGameState.isWin() or currentGameState.isLose() or now_depth > self.depth:
                return self.evaluationFunction(currentGameState), 0
            if agentIndex == 0:
                return max_value(currentGameState, now_depth, agentIndex)
            else:
                return expected_value(currentGameState, now_depth, agentIndex)

        def max_value(currentGameState, now_depth, agentIndex):

            legalMoves = currentGameState.getLegalActions()
            NextState = [currentGameState.getNextState(
                agentIndex, action) for action in legalMoves]
            stateValue = [value(nextState, now_depth, agentIndex)[0]
                          for nextState in NextState]

            v = max(stateValue)
            val_indice = [index for index in range(
                len(stateValue)) if stateValue[index] == v]
            chosenIndex = random.choice(val_indice)

            return v, legalMoves[chosenIndex]

        def expected_value(currentGameState, now_depth, agentIndex):

            legalMoves = currentGameState.getLegalActions(agentIndex)
            NextState = [currentGameState.getNextState(
                agentIndex, action) for action in legalMoves]

            expect_value = 0
            for nextState in NextState:
                expect_value += (value(nextState, now_depth,
                                       agentIndex)[0] / len(NextState))
            action = random.choice(legalMoves)

            return expect_value, action

        (v, action) = value(gameState, 1, -1)
        return action
        raise NotImplementedError("To be implemented")
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
        The idea my evaluation function is pretty simple, I initialize the value to 
    zero and use four factors to determine it. 
    1. "Win/Lose" is the end of the game, so we directly return positive/negative 
        infinite. 
    2. "The remaining number of food" would mainly affect the action of pacman. This 
        factor makes the pacman tend to eat food.
    3. "Letting ghost be scared". As we know, eating scared ghost will get much score. 
        So, this factor would make the pacman eat the capsule if it finds any capsules 
        nearby.
    4. "The min distance between pacman and ghost" can affect the action of pacman 
        slightly. This factor let pacman would not stay in place when there is no food 
        around it, or get as close to the ghost as possible when the ghost is scared.
    """
    pos = currentGameState.getPacmanPosition()
    GhostStates = currentGameState.getGhostStates()
    minGhostDistance = min(
        [manhattanDistance(pos, state.getPosition()) for state in GhostStates])

    value = 0
    if currentGameState.isWin():
        value = float('inf')
        return value
    elif currentGameState.isLose():
        value = float('-inf')
        return value

    value -= currentGameState.getNumFood()
    value -= (minGhostDistance / 25000)

    for state in GhostStates:
        if state.scaredTimer > 0:
            value += 1

    return value

    raise NotImplementedError("To be implemented")
    # End your code (Part 4)


# Abbreviation
better = betterEvaluationFunction
