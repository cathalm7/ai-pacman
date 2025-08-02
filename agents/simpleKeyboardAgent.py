# simpleKeyboardAgent.py
# ---------------------
# A simple keyboard agent that doesn't rely on tkinter
# Uses standard input for keyboard controls

import sys
import os
import threading
import time
from collections import deque

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.game import Agent
from core.game import Directions
import random


class SimpleKeyboardAgent(Agent):
    """
    A simple keyboard agent that uses standard input instead of tkinter.
    This allows keyboard controls without requiring tkinter.
    """

    # Key mappings
    WEST_KEY = "a"
    EAST_KEY = "d"
    NORTH_KEY = "w"
    SOUTH_KEY = "s"
    STOP_KEY = "q"

    def __init__(self, index=0):
        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []
        self.input_thread = None
        self.running = True
        self.input_queue = deque()

        # Start input thread
        self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
        self.input_thread.start()

    def _input_loop(self):
        """Background thread to capture keyboard input"""
        if os.name == "nt":
            import msvcrt
        else:
            import tty
            import termios

        if os.name == "nt":  # Windows
            while self.running:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode("utf-8").lower()
                    self.input_queue.append(key)
                time.sleep(0.01)
        else:  # Unix/Linux/macOS
            import tty
            import termios

            # Save terminal settings
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)

            try:
                # Set terminal to raw mode
                tty.setraw(sys.stdin.fileno())

                while self.running:
                    if sys.stdin.readable():
                        key = sys.stdin.read(1).lower()
                        self.input_queue.append(key)
                    time.sleep(0.01)
            finally:
                # Restore terminal settings
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def getAction(self, state):
        """Get the next action based on keyboard input"""
        # Process any pending input
        while self.input_queue:
            key = self.input_queue.popleft()
            if key in [
                self.WEST_KEY,
                self.EAST_KEY,
                self.NORTH_KEY,
                self.SOUTH_KEY,
                self.STOP_KEY,
            ]:
                self.keys = [key]

        legal = state.getLegalActions(self.index)
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

    def __del__(self):
        """Clean up when agent is destroyed"""
        self.running = False
        if self.input_thread and self.input_thread.is_alive():
            self.input_thread.join(timeout=0.1)


class SimpleKeyboardAgent2(SimpleKeyboardAgent):
    """
    A second simple keyboard agent with different key mappings.
    """

    # Different key mappings for second player
    WEST_KEY = "j"
    EAST_KEY = "l"
    NORTH_KEY = "i"
    SOUTH_KEY = "k"
    STOP_KEY = "u"
