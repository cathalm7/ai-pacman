# basicKeyboardAgent.py
# --------------------
# A basic keyboard agent that uses simple input() for keyboard controls
# No tkinter required - works with any Python installation

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game import Agent
from core.game import Directions
import random


class BasicKeyboardAgent(Agent):
    """
    A basic keyboard agent that uses input() for keyboard controls.
    This is the simplest approach that doesn't require tkinter.

    Note: This requires pressing Enter after each key press.
    """

    # Key mappings
    WEST_KEY = "a"
    EAST_KEY = "d"
    NORTH_KEY = "w"
    SOUTH_KEY = "s"
    STOP_KEY = "q"
    QUIT_KEY = "x"

    def __init__(self, index=0):
        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []
        print("Basic Keyboard Agent initialized!")
        print("Controls: w/a/s/d to move, q to stop, x to quit")
        print("Note: Press Enter after each key press")

    def getAction(self, state):
        """Get the next action based on keyboard input"""
        legal = state.getLegalActions(self.index)

        # Get user input
        try:
            key = input("Enter move (w/a/s/d/q/x): ").lower().strip()

            # Handle quit
            if key == self.QUIT_KEY:
                print("Quitting game...")
                sys.exit(0)

            # Store the key
            self.keys = [key] if key else []

        except (EOFError, KeyboardInterrupt):
            print("\nQuitting game...")
            sys.exit(0)

        # Get move based on input
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal:
            move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self, legal):
        """Convert key presses to moves"""
        move = Directions.STOP

        if self.WEST_KEY in self.keys and Directions.WEST in legal:
            move = Directions.WEST
        if self.EAST_KEY in self.keys and Directions.EAST in legal:
            move = Directions.EAST
        if self.NORTH_KEY in self.keys and Directions.NORTH in legal:
            move = Directions.NORTH
        if self.SOUTH_KEY in self.keys and Directions.SOUTH in legal:
            move = Directions.SOUTH

        return move


class BasicKeyboardAgent2(BasicKeyboardAgent):
    """
    A second basic keyboard agent with different key mappings.
    """

    # Different key mappings for second player
    WEST_KEY = "j"
    EAST_KEY = "l"
    NORTH_KEY = "i"
    SOUTH_KEY = "k"
    STOP_KEY = "u"
    QUIT_KEY = "x"
