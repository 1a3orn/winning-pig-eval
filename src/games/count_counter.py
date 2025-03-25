from typing import List, Tuple
import copy
from dataclasses import dataclass

from mcts.abstract_game import AbstractGameState

@dataclass
class Position:
    row: int
    col: int

class CoinCounterGridState(AbstractGameState):
    def __init__(self, grid: List[List[int]] = None, player_to_move: int = 0):
        """
        Initialize the game state.
        grid: 3x3 grid where each cell contains number of coins (0-3)
        player_to_move: 0 or 1, indicating whose turn it is
        """
        self.grid = grid if grid is not None else [[0 for _ in range(3)] for _ in range(3)]
        self._player_to_move = player_to_move

    def get_short_game_description(self) -> str:
        return """\
Two players take turns placing coins on a 3x3 grid. Each player places one coin per move, and up to a total of three coins can be placed per spot in the grid. If your move makes three-in-a-row of 1 coins, 2 coins, or 3 coins, then you win.
"""

    def get_name(self) -> str:
        return "Coin Counter"

    def get_detailed_rules(self) -> str:
        return """\
        Start condition: An empty 3 x 3 grid.
        Rules:
        - Two players alternate turns, until one player wins.
        - Each player places on coin on a spot in the grid per turn, which increases the number of coins in that spot by 1.
        - The maximum number of coins per spot is 3.
        - A player wins if they make a row of 1-1-1, 2-2-2, or 3-3-3 coins in a row.
        - The row may be horizontal, vertical, or along the diagonal.
        """

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal moves in format 'row,col'"""
        actions = []
        for row in range(3):
            for col in range(3):
                if self.grid[row][col] < 3:  # Can add a coin if less than 3 coins
                    actions.append(f"{row},{col}")
        return actions

    def take_action(self, action: str) -> 'CoinCounterGridState':
        """Takes action in format 'row,col' and returns new state"""
        row, col = map(int, action.split(','))
        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError("Invalid position")
        if self.grid[row][col] >= 3:
            raise ValueError("Cannot place more than 3 coins in a position")

        # Create new state with updated grid
        new_grid = copy.deepcopy(self.grid)
        new_grid[row][col] += 1
        return CoinCounterGridState(new_grid, 1 - self._player_to_move)

    def _check_win(self) -> bool:
        """Check if current state is a win for either player"""
        # Check rows
        for row in range(3):
            if self.grid[row][0] > 0 and self.grid[row][0] == self.grid[row][1] == self.grid[row][2]:
                return True

        # Check columns
        for col in range(3):
            if self.grid[0][col] > 0 and self.grid[0][col] == self.grid[1][col] == self.grid[2][col]:
                return True

        # Check diagonals
        if self.grid[0][0] > 0 and self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
            return True
        if self.grid[0][2] > 0 and self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
            return True

        return False

    def is_terminal(self) -> bool:
        """Returns True if game is over"""
        if self._check_win():
            return True
        
        # Check if grid is full (no more legal moves)
        return len(self.get_legal_actions()) == 0

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        if self._check_win():
            # If it's player 1's turn, player 0 just moved and won
            if self._player_to_move == 1:
                return (1.0, -1.0)
            # If it's player 0's turn, player 1 just moved and won
            else:
                return (-1.0, 1.0)
        
        # If no winner but game is terminal, it's a draw
        return (0.0, 0.0)

    def get_player_to_move(self) -> int:
        return self._player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        result = f"Player {self._player_to_move}'s turn\n"
        for row in range(3):
            result += " | ".join(str(cell) for cell in self.grid[row])
            if row < 2:
                result += "\n---------\n"
        return result