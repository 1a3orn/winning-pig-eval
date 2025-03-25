from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class Chomp(AbstractGameState):
    def __init__(self, size: int = 4, grid: List[List[bool]] = None, player_to_move: int = 0):
        # Initialize NxN grid, True means chocolate piece exists
        self.size = size
        self.grid = grid if grid is not None else [[True]*size for _ in range(size)]
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return f"Chomp {self.size}x{self.size}"

    def get_short_game_description(self) -> str:
        return f"""
A game played on a {self.size}x{self.size} chocolate grid. Players take turns eating chocolate pieces, which also removes
all pieces below and to the right. The player forced to eat the poisoned piece (0,0) loses.
"""

    def get_detailed_rules(self) -> str:
        return f"""
Start condition: A {self.size}x{self.size} grid of chocolate pieces, with the piece at (0,0) being poisoned.

Rules:
- Two players alternate turns
- On your turn, you must choose an existing chocolate piece to eat
- The rows and columns are 0-indexed, starting from top-left.
- When you eat a piece at position (x,y), you also eat all pieces at positions (i,j) where i≥x and j≥y
- Thus if you eat (2,2), you also eat all pieces below and to the right of it.
- The piece at (0,0) is poisoned
- The player who is forced to eat the poisoned piece (0,0) LOSES
- You must take a bite on your turn if possible

To make a move, specify the position as 'row,col' (e.g., '1,2')
Positions are 0-indexed, starting from top-left.
"""

    def get_legal_actions(self) -> List[str]:
        actions = []
        # Eat all pieces below and to the right
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j]:
                    actions.append(f"{i},{j}")
        return actions

    def take_action(self, action: str) -> 'Chomp':
        row, col = map(int, action.split(','))
        if (0 > row or row >= self.size or 0 > col or col >= self.size):
            raise ValueError("Invalid position")
        if not self.grid[row][col]:
            raise ValueError("Position already eaten")

        new_grid = [row.copy() for row in self.grid]
        # Eat all pieces below and to the right
        for i in range(row, self.size):
            for j in range(col, self.size):
                new_grid[i][j] = False

        return Chomp(self.size, new_grid, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        return not self.grid[0][0]

    def get_result(self) -> Tuple[float, float]:
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # If it's player 1's turn, player 0 just moved and lost (ate 0,0)
        # If it's player 0's turn, player 1 just moved and lost (ate 0,0)
        if not self.grid[0][0]:
            return (-1.0, 1.0) if self.player_to_move == 0 else (1.0, -1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        result = f"Turn: Player {self.player_to_move}\n"
        result += "Chocolate Grid:\n"
        for i in range(self.size):
            result += "  "
            for j in range(self.size):
                result += "■ " if self.grid[i][j] else "· "
            result += "\n"
        return result
