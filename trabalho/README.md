# Dameo Project

> **Authors**
> Beatriz Oliveira (202403546)
> Pedro Magalhães (202403859)
> Rodrigo Dias (202407281)

## Table of Contents

- [About the Project](#about-the-project)
- [Game Rules](#game-rules)
- [How to Run the Project](#how-to-run-the-project)
- [Difficulty Levels](#difficulty-levels)
- [Technical Requirements](#technical-requirements)
- [Project Structure](#project-structure)

---

## About the Project

This project was developed during the first year of the Bachelor's degree in Artificial Intelligence and Data Science at the Faculty of Sciences of the University of Porto. The challenge was to develop an artificial intelligence capable of playing a board game — we chose **Dameo**, which is a modern variant of checkers.

We created an application with several game modes (PvP, PvAI, AIvAI) and multiple AI difficulty levels, with different implementations of the **Minimax** algorithm (with and without Alpha-Beta pruning).

---

## Game Rules

- The player with blue pieces is the one who starts;
- The pieces can only move forward, either straight ahead or diagonally 
and, if the square right next to them is occupied, they can jump over other 
pieces of their color on the same direction until they find an empty square;
- When a piece’s last move ends on the opposite side of the board, it becomes a king;
- The captures can only be made orthogonally and, if it is possible, it must be done;
- A king can move in eight directions, to any available square, never jumping over 
a piece of its color;
- Multi-captures must be done if, after a capture, there are others possible by the same piece;
- The same piece can’t be jumped more than once;
- The game ends when one of the players has no pieces left.

---

## How to Run the Project

### 1. Download the Project

Clone or download the GitHub repository and extract the contents.

```bash
git clone gh repo clone PedroM08/Dameo_Project

https://github.com/PedroM08/Dameo_Project.git

```

### 2. Open in your preferred editor

For example, VSCode, Pycharm, ...

### 3. Install dependencies

Install Pygame:

```bash
pip install pygame
```

### 4. Run the game

Make sure you are in the /trabalho directory
Run the `main.py` file:

```bash
python main.py
```

---

## Difficulty Levels

In **PvAI** and **AIvAI** modes, you can choose different AI levels:

| Level | Name                | Description                                               |
|-------|---------------------|-----------------------------------------------------------|
| 0     | `RandomAI`          | Makes random moves with no strategy                      |
| 1     | `Minimax1`          | Basic Minimax algorithm with depth 2                     |
| 2     | `Minimax2`          | Minimax with additional heuristics (progression to king) |
| 3     | `MinimaxAlphaBeta`  | Minimax with Alpha-Beta pruning and depth 4              |

---

## Technical Requirements

- Python 3.9 or higher
- Pygame (version 2.0 or higher)
- Operating System: Windows / macOS / Linux

---

## Project Structure

```
packages/
│   ├── board.py            # Board logic and valid moves
│   ├── piece.py            # Piece class (men and kings)
│   ├── game.py             # Main game mechanics
│   ├── ai_player.py        # Random AI (level 0)
│   ├── minimax_1.py        # Basic Minimax (level 1)
│   ├── minimax_2.py        # Minimax with heuristics (level 2)
│   ├── minimax_3.py        # Minimax with Alpha-Beta pruning (level 3)
│   └── constants.py        # Visual constants and images
|
images/                     # All images used in the game
main.py                     # Main script to run the game
README.md                   # This file
```

---
