# multiAgents.py
# --------------


import random
import math
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import util
from core.game import Agent


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
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Set up stating score from previous state
        score = successorGameState.getScore()

        foodDistances = []
        for food in newFood.asList():
            # Get manhattanDistance between new position and every food
            foodDistances.append(util.manhattanDistance(newPos, food))
        if len(foodDistances):
            # if foodDistances not empty
            # food score is the mean of food distance from new position
            foodScore = sum(foodDistances) / len(foodDistances)
        else:
            foodScore = 1

        ghostDistances = []
        scaredGhostDistances = []
        dangerousGhostDistances = []

        for i, ghost in enumerate(newGhostStates):
            ghostDistance = util.manhattanDistance(newPos, ghost.getPosition())
            ghostDistances.append(ghostDistance)

            # Check if this ghost is scared
            if newScaredTimes[i] > 0:
                # Ghost is scared - we want to pursue it
                scaredGhostDistances.append(ghostDistance)
            else:
                # Ghost is dangerous - we want to avoid it
                dangerousGhostDistances.append(ghostDistance)

        # Handle scared ghosts - strongly encourage pursuit
        if scaredGhostDistances:
            closestScaredGhost = min(scaredGhostDistances)
            # Strong positive reward for being close to scared ghosts
            # The closer the better, with exponential reward
            score += 200 / (closestScaredGhost + 1)  # +1 to avoid division by zero

        # Handle dangerous ghosts - avoid them
        if dangerousGhostDistances:
            closestDangerousGhost = min(dangerousGhostDistances)
            if closestDangerousGhost <= 2:
                # Strong penalty for being too close to dangerous ghosts
                score -= 1000 / (closestDangerousGhost + 1)

        # Food consideration - prefer closer food
        if foodDistances:
            closestFood = min(foodDistances)
            score += 10 / (closestFood + 1)  # Reward for being close to food

        return score


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

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
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

        def baseCase(gameState, depth):
            # Base Case - Game is Over or reached max depth
            # Stop recursion if any is true
            return gameState.isWin() or gameState.isLose() or (depth == self.depth)

        def minimax(gameState, agentIndex, depth):
            if baseCase(gameState, depth):
                return self.evaluationFunction(gameState), ""

            elif agentIndex == 0:
                # Want to maxize Pacman (evalScore the hight the better)
                node = maxValue(gameState, agentIndex, depth)
            else:
                # Minimize the ghosts actions
                node = minValue(gameState, agentIndex, depth)
            return node

        def minValue(gameState, agentIndex, depth):
            val = math.inf
            act = ""

            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    # Recursed in All agent. Back to pacman in new depth
                    node = minimax(
                        gameState.generateSuccessor(agentIndex, action), 0, depth + 1
                    )
                else:
                    # Recurse in next ghost
                    node = minimax(
                        gameState.generateSuccessor(agentIndex, action),
                        agentIndex + 1,
                        depth,
                    )

                # Find action that minimize val
                if val > node[0]:
                    val = node[0]
                    act = action
            return val, act

        def maxValue(gameState, agentIndex, depth):
            val = -math.inf
            act = ""

            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    # Recursed in All agent. Back to pacman in new depth
                    node = minimax(
                        gameState.generateSuccessor(agentIndex, action), 0, depth + 1
                    )
                else:
                    # Recurse in next ghost
                    node = minimax(
                        gameState.generateSuccessor(agentIndex, action),
                        agentIndex + 1,
                        depth,
                    )

                # Find action that maximize val
                if val < node[0]:
                    val = node[0]
                    act = action
            return val, act

        return minimax(gameState, agentIndex=0, depth=0)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def baseCase(gameState, depth):
            # Base Case - Game is Over or reached max depth
            # Stop recursion if any is true
            return gameState.isWin() or gameState.isLose() or (depth == self.depth)

        def alphaBeta(gameState, agentIndex, depth, alpha, beta):
            if baseCase(gameState, depth):
                return self.evaluationFunction(gameState), ""

            elif agentIndex == 0:
                # Want to maxize Pacman (evalScore the hight the better)
                node = maxValue(gameState, agentIndex, depth, alpha, beta)
            else:
                # Minimize the ghosts actions
                node = minValue(gameState, agentIndex, depth, alpha, beta)
            return node

        def minValue(gameState, agentIndex, depth, alpha, beta):
            val = math.inf
            act = ""

            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    # Recursed in All agent. Back to pacman in new depth
                    node = alphaBeta(
                        gameState.generateSuccessor(agentIndex, action),
                        0,
                        depth + 1,
                        alpha,
                        beta,
                    )
                else:
                    # Recurse in next ghost
                    node = alphaBeta(
                        gameState.generateSuccessor(agentIndex, action),
                        agentIndex + 1,
                        depth,
                        alpha,
                        beta,
                    )

                # Find action that minimize val
                if val > node[0]:
                    val = node[0]
                    act = action

                if node[0] < alpha:
                    # Prunning
                    return val, act
                beta = min(node[0], beta)

            return val, act

        def maxValue(gameState, agentIndex, depth, alpha, beta):
            val = -math.inf
            act = ""

            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    # Recursed in All agent. Back to pacman in new depth
                    node = alphaBeta(
                        gameState.generateSuccessor(agentIndex, action),
                        0,
                        depth + 1,
                        alpha,
                        beta,
                    )
                else:
                    # Recurse in next ghost
                    node = alphaBeta(
                        gameState.generateSuccessor(agentIndex, action),
                        agentIndex + 1,
                        depth,
                        alpha,
                        beta,
                    )

                # Find action that maximize val
                if val < node[0]:
                    val = node[0]
                    act = action

                if node[0] > beta:
                    # Prunning
                    return val, act
                alpha = max(node[0], alpha)
            return val, act

        return alphaBeta(
            gameState, agentIndex=0, depth=0, alpha=-math.inf, beta=math.inf
        )[1]


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

        def baseCase(gameState, depth):
            # Base Case - Game is Over or reached max depth
            # Stop recursion if any is true
            return gameState.isWin() or gameState.isLose() or (depth == self.depth)

        def expectiMax(gameState, agentIndex, depth):
            if baseCase(gameState, depth):
                return self.evaluationFunction(gameState), ""

            elif agentIndex == 0:
                # Want to maxize Pacman (evalScore the hight the better)
                node = maxValue(gameState, agentIndex, depth)
            else:
                # specificity of expectiminimax
                node = helper(gameState, agentIndex, depth)
            return node

        def helper(gameState, agentIndex, depth):
            prob = 0
            fraction = 1 / len(gameState.getLegalActions(agentIndex))

            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    # Recursed in All agent. Back to pacman in new depth
                    nodeValue = expectiMax(
                        gameState.generateSuccessor(agentIndex, action),
                        0,
                        depth + 1,
                    )[0]
                else:
                    # Recurse in next ghost
                    nodeValue = expectiMax(
                        gameState.generateSuccessor(agentIndex, action),
                        agentIndex + 1,
                        depth,
                    )[0]

                # Accumulate expected value
                prob += fraction * nodeValue

            return prob, ""

        def maxValue(gameState, agentIndex, depth):
            val = -math.inf
            act = ""

            for action in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    # Recursed in All agent. Back to pacman in new depth
                    node = expectiMax(
                        gameState.generateSuccessor(agentIndex, action), 0, depth + 1
                    )
                else:
                    # Recurse in next ghost
                    node = expectiMax(
                        gameState.generateSuccessor(agentIndex, action),
                        agentIndex + 1,
                        depth,
                    )

                # Find action that maximize val
                if val < node[0]:
                    val = node[0]
                    act = action
            return val, act

        return expectiMax(gameState, agentIndex=0, depth=0)[1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Enhanced evaluation function that properly handles scared ghosts,
                 capsules, and food collection with strategic priorities.
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newCapsule = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Set up stating score from previous state
    score = currentGameState.getScore()

    # Calculate food distances
    foodDistances = []
    for food in newFood.asList():
        foodDistances.append(util.manhattanDistance(newPos, food))

    if foodDistances:
        closestFood = min(foodDistances)
        # Reward for being close to food
        score += 10 / (closestFood + 1)
    else:
        closestFood = 1

    # Calculate capsule distances
    capsuleDistances = []
    for capsule in newCapsule:
        capsuleDistances.append(util.manhattanDistance(newPos, capsule))

    if capsuleDistances:
        closestCapsule = min(capsuleDistances)
        # Strong reward for being close to capsules (they make ghosts scared)
        score += 50 / (closestCapsule + 1)

    # Handle ghosts - separate scared and dangerous ghosts
    scaredGhostDistances = []
    dangerousGhostDistances = []

    for i, ghost in enumerate(newGhostStates):
        ghostDistance = util.manhattanDistance(newPos, ghost.getPosition())

        # Check if this ghost is scared
        if newScaredTimes[i] > 0:
            # Ghost is scared - we want to pursue it
            scaredGhostDistances.append(ghostDistance)
        else:
            # Ghost is dangerous - we want to avoid it
            dangerousGhostDistances.append(ghostDistance)

    # Handle scared ghosts - strongly encourage pursuit
    if scaredGhostDistances:
        closestScaredGhost = min(scaredGhostDistances)
        # Very strong positive reward for being close to scared ghosts
        # Eating a ghost gives +200 points, so we want to prioritize this
        score += 300 / (closestScaredGhost + 1)

    # Handle dangerous ghosts - avoid them
    if dangerousGhostDistances:
        closestDangerousGhost = min(dangerousGhostDistances)
        if closestDangerousGhost <= 3:
            # Strong penalty for being too close to dangerous ghosts
            score -= 2000 / (closestDangerousGhost + 1)

    # Bonus for having few remaining food pellets
    remainingFood = len(foodDistances)
    if remainingFood <= 5:
        # Extra reward when close to winning
        score += (10 - remainingFood) * 50

    return score


# Abbreviation
better = betterEvaluationFunction
