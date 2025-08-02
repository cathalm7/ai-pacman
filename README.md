# 🎮 AI Pacman - Multi-Agent Search Algorithms

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](#-license)
[![AI](https://img.shields.io/badge/AI-Multi--Agent%20Search-orange.svg)](#-project-overview)

<details>
<summary><strong>📋 Table of Contents</strong></summary>
<br>

- [📖 Project Overview](#-project-overview)
- [🚀 Getting Started](#-getting-started)
  - [📋 Prerequisites](#-prerequisites)
  - [🔧 Installation](#-installation)
  - [🎮 Two Modes](#-two-modes)
  - [🎮 Game Controls](#-game-controls)
  - [🗺️ Available Layouts](#️-available-layouts)
- [👥 Multi-Agent Search Overview](#-multi-agent-search-overview)
  - [🧠 Implemented Algorithms](#-implemented-algorithms)
  - [👻 Ghost Behaviors](#-ghost-behaviors)
- [📁 Project Structure](#-project-structure)
- [📄 License](#-license)

</details>

---

## 📖 Project Overview

> **🎯 Goal**: Demonstrate advanced artificial intelligence concepts through the classic Pacman game

This project was developed for a final AI course project at **University of Arizona**, focusing on **multi-agent search algorithms** and adversarial game playing.


<table>
<tr>
<td width="50%">

**🤖 AI Mode**
- Watch algorithms compete
- Compare performance

</td>
<td width="50%">

**🎯 Interactive Mode**
- Play the game yourself
- Experience classic Pacman

</td>
</tr>
</table>

---

## 🚀 Getting Started

### 🔧 Installation

```bash
# Install Python 3.11 with Tkinter support
brew install python-tk@3.11

# Clone and run
git clone <repository-url>
cd ai-pacman
```

### 🎮 Two Modes

**🤖 AI Demo Mode - Watch Algorithms Play**
```bash
# python3.11 examples/demo.py [algorithm] [layout]
un run examples/demo.py expectimax powerClassic
```

**🎯 Interactive Mode - Play Yourself**
```bash
# python3.11 play_pacman.py [layout]
un run play_pacman.py mediumClassic
```

### 🎮 Game Controls

| Input | Action |
|-------|--------|
| **WASD** or **Arrow Keys** | Move Pacman |
| **Q** | Quit game |
| **Click Window** | Focus for input |

### 🗺️ Available Layouts

| Layout | Description |
|--------|-------------|
| `smallClassic` | Quick games, small maze |
| `mediumClassic` | Standard size, balanced gameplay |
| `openClassic` | Open maze with fewer walls |
| `minimaxClassic` | Designed for algorithm testing |
| `trappedClassic` | Complex maze with tight corridors |
| `trickyClassic` | Advanced layout with strategic challenges |


## 👥 Multi-Agent Search Overview

### 😎 Pacman Logic

#### 🎯 `minimax` Algorithm
**Core Concept**: Zero-sum game theory

- **Pacman** (maximizing player) tries to maximize score
- **Ghosts** (minimizing players) try to minimize Pacman's score  
- Uses depth-limited search to explore possible game states
- Returns the best action for Pacman based on worst-case ghost behavior

#### ⚡ `alphabeta` Pruning
**Core Concept**: Optimized minimax with branch elimination

- Prunes irrelevant branches during search
- Significantly reduces computation time
- Maintains optimal decisions
- **Best choice for most use cases**

#### 🎲 `expectimax` Algorithm
**Core Concept**: Probabilistic opponent modeling

- Handles probabilistic ghost behavior (random actions)
- Pacman maximizes expected value instead of worst-case
- More realistic for games with uncertainty
- Balances risk and reward

### 👻 Ghost Behaviors

- **AI Demo Mode**: Ghosts use optimal strategy against algorithms (Minimax/Alpha-Beta) or are modeled as probabilistic (Expectimax)
- **Interactive Mode**: Smart adaptive AI that hunts Pacman and flees when scared after power pellets
---

## 📁 Project Structure

```
🎮 ai-pacman/
├── README.md                 # Project documentation
├── play_pacman.py           # Interactive play launcher
├── algorithms/
│   └── multi_agents.py         # Multi-agent search algorithms
├── core/
│   ├── game.py                 # Core game mechanics
│   ├── pacman.py               # Pacman game logic
│   ├── util.py                 # Utility functions
│   ├── layout.py               # Layout parsing
│   └── ghostAgents.py          # Ghost AI implementations
├── display/
│   ├── graphicsDisplay.py      # Graphical display
│   ├── graphicsUtils.py        # Graphics utilities
│   └── textDisplay.py          # Text-based display
├── layouts/                # Game layout files (.lay)
├── examples/
│   └── demo.py                 # AI demo script
└── agents/
    ├── pacmanAgents.py         # Pacman agent implementations
    ├── keyboardAgents.py       # Keyboard input agents
    └── basicKeyboardAgent.py   # Simple keyboard agent
```

---

## 📄 License

📚 Educational Use Only: This project is designed for learning and educational purposes.
