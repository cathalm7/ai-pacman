#!/usr/bin/env python3
"""
Pacman Game Launcher with Graphics and Keyboard Controls
=======================================================

This script launches the Pacman game with keyboard controls.
It will try to use full graphics if tkinter is available,
otherwise falls back to text display with basic keyboard input.

Usage:
    python play_pacman.py [layout]

Available layouts:
    - smallClassic
    - mediumClassic
    - originalClassic
    - testClassic
    - minimaxClassic
    - powerClassic
    - capsuleClassic
    - contestClassic
    - trappedClassic
    - trickyClassic

Controls:
    Graphics mode: WASD or Arrow Keys to move, Q to stop
    Text mode: w/a/s/d to move, q to stop, x to quit (press Enter after each key)
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import game components
from core.pacman import runGames
from core.layout import getLayout
from core.ghostAgents import RandomGhost, DirectionalGhost

# Try to import graphics components
try:
    from display.graphicsDisplay import PacmanGraphics
    from agents.keyboardAgents import KeyboardAgent

    GRAPHICS_AVAILABLE = True
    print("✓ Graphics mode available - using full Pacman graphics!")
    print("   Graphics window will open in a few seconds...")
except ImportError as e:
    print("⚠ Graphics mode not available - using text display")
    print("   To enable graphics, install tkinter properly:")
    print("   - On macOS: brew install python-tk")
    print("   - On Ubuntu: sudo apt-get install python3-tk")
    print("   - On Windows: tkinter usually comes with Python")
    print()
    from display.textDisplay import PacmanGraphics
    from agents.basicKeyboardAgent import BasicKeyboardAgent as KeyboardAgent

    GRAPHICS_AVAILABLE = False


def print_usage():
    """Print usage information"""
    print(__doc__)


def get_default_layout():
    """Get default layout if none specified"""
    return "smallClassic"


def main():
    """Main function to run the game with keyboard controls"""
    # Parse command line arguments
    if len(sys.argv) > 2:
        print("Error: Too many arguments")
        print_usage()
        return

    # Get layout name
    if len(sys.argv) == 2:
        layout_name = sys.argv[1]
    else:
        layout_name = get_default_layout()
        print(f"No layout specified, using default: {layout_name}")

    # Validate and get layout
    try:
        layout = getLayout(layout_name)
    except Exception as e:
        print(f"Error: Invalid layout '{layout_name}'")
        print(
            "Available layouts: smallClassic, mediumClassic, originalClassic, testClassic, minimaxClassic, powerClassic, capsuleClassic, contestClassic, trappedClassic, trickyClassic"
        )
        return

    # Set up agents
    pacman = KeyboardAgent(0)  # Keyboard-controlled Pacman
    ghosts = [DirectionalGhost(i + 1) for i in range(2)]  # Two directional ghosts

    # Set up display
    graphics = PacmanGraphics()

    print(f"\nStarting Pacman game with keyboard controls...")
    print(f"Layout: {layout_name}")

    if GRAPHICS_AVAILABLE:
        print("Controls: WASD or Arrow Keys to move, Q to stop")
        print("Graphics window will open - click on it to focus for keyboard input")
        print("If you don't see the window, check behind other windows or try Cmd+Tab")
    else:
        print("Controls: w/a/s/d to move, q to stop, x to quit")
        print("Note: Press Enter after each key press")

    print("=" * 60)

    # Run the game
    try:
        runGames(
            layout=layout,
            pacman=pacman,
            ghosts=ghosts,
            display=graphics,
            numGames=1,
            record=False,
            catchExceptions=False,
        )
        print("\nGame completed!")
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Error running game: {e}")


if __name__ == "__main__":
    main()
