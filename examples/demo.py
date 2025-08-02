#!/usr/bin/env python3
"""
AI Pacman Demo Script
=====================

This script demonstrates how to use the different multi-agent search algorithms
implemented in the AI Pacman project.

Usage:
    python demo.py [algorithm] [layout]

Available algorithms:
    - minimax: Minimax algorithm
    - alphabeta: Alpha-beta pruning
    - expectimax: Expectimax algorithm

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
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pacman import runGames
from core.layout import getLayout
from display.graphicsDisplay import PacmanGraphics
from core.ghostAgents import DirectionalGhost
from algorithms.multi_agents import MinimaxAgent, AlphaBetaAgent, ExpectimaxAgent


def print_usage():
    """Print usage information"""
    print(__doc__)
    print("\nExamples:")
    print("  python demo.py minimax smallClassic")
    print("  python demo.py alphabeta mediumClassic")
    print("  python demo.py expectimax originalClassic")


def get_agent(algorithm_name):
    """Get the appropriate agent based on algorithm name"""
    if algorithm_name == "minimax":
        return MinimaxAgent(evalFn="betterEvaluationFunction", depth="2")
    elif algorithm_name == "alphabeta":
        return AlphaBetaAgent(evalFn="betterEvaluationFunction", depth="2")
    elif algorithm_name == "expectimax":
        return ExpectimaxAgent(evalFn="betterEvaluationFunction", depth="2")
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")


def main():
    """Main demo function"""
    if len(sys.argv) != 3:
        print_usage()
        return

    algorithm = sys.argv[1]
    layout_name = sys.argv[2]

    # Validate algorithm
    valid_algorithms = ["minimax", "alphabeta", "expectimax"]
    if algorithm not in valid_algorithms:
        print(f"Error: Invalid algorithm '{algorithm}'")
        print(f"Valid algorithms: {', '.join(valid_algorithms)}")
        return

    # Validate layout
    try:
        layout = getLayout(layout_name)
    except Exception as e:
        print(f"Error: Invalid layout '{layout_name}'")
        print(
            "Available layouts: smallClassic, mediumClassic, originalClassic, testClassic, minimaxClassic, powerClassic, capsuleClassic, contestClassic, trappedClassic, trickyClassic"
        )
        return

    # Get the agent
    try:
        pacman = get_agent(algorithm)
    except Exception as e:
        print(f"Error creating agent: {e}")
        return

    # Set up ghosts
    ghosts = [DirectionalGhost(i + 1) for i in range(2)]

    # Run the game
    print(f"\nRunning {algorithm.upper()} algorithm on {layout_name} layout...")
    print("=" * 50)

    try:
        # Use visual graphics instead of null graphics
        graphics = PacmanGraphics(frameTime=0.1)  # 0.1 second delay between frames
        runGames(layout, pacman, ghosts, graphics, numGames=1, record=False)
        print("\nGame completed successfully!")
    except Exception as e:
        print(f"Error running game: {e}")


if __name__ == "__main__":
    main()
