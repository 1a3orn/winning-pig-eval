from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class Domineering(AbstractGameState):
    def __init__(self, size: int = 4, board: List[List[bool]] = None, player_to_move: int = 0):
        # Validate board size
        if size < 2:
            raise ValueError("Board size must be at least 2x2")
        self.size = size
        
        # Initialize NxN board (True = empty space, False = occupied)
        self.board = board if board is not None else [[True] * size for _ in range(size)]
        if len(self.board) != size or any(len(row) != size for row in self.board):
            raise ValueError(f"Board must be {size}x{size}")
        self.player_to_move = player_to_move
        # Player 0 places vertical dominos, Player 1 places horizontal dominos
        
    def get_name(self) -> str:
        return f"Domineering ({self.size}x{self.size})"

    def get_short_game_description(self) -> str:
        return f"""
A game played on a {self.size}x{self.size} grid where players alternate placing dominos. 
Player 0 places vertical dominos (2x1), Player 1 places horizontal dominos (1x2).
The last player to make a legal move wins.
"""

    def get_detailed_rules(self) -> str:
        return f"""
Start condition: Empty {self.size}x{self.size} grid

Rules:
- Two players alternate turns
- Player 0 places vertical dominos (occupying two rows in one column)
- Player 1 places horizontal dominos (occupying two columns in one row)
- Dominos cannot overlap or extend beyond the board
- A player who cannot make a legal move loses
- Important: The last player to make a legal move WINS

To make a move, specify the top-left coordinate of where you want to place your domino:
- Format: 'row,col'
- Coordinates are 0-indexed from top-left
- Example: '1,2' means:
  - For Player 0: vertical domino starting at row 1, column 2
  - For Player 1: horizontal domino starting at row 1, column 2
"""

    def get_legal_actions(self) -> List[str]:
        actions = []
        
        if self.player_to_move == 0:  # Vertical dominos
            for col in range(self.size):
                for row in range(self.size - 1):  # Only up to second-to-last row
                    if self.board[row][col] and self.board[row + 1][col]:
                        actions.append(f"{row},{col}")
        else:  # Horizontal dominos
            for row in range(self.size):
                for col in range(self.size - 1):  # Only up to second-to-last column
                    if self.board[row][col] and self.board[row][col + 1]:
                        actions.append(f"{row},{col}")
        
        return actions

    def take_action(self, action: str) -> 'Domineering':
        row, col = map(int, action.split(','))
        new_board = [row.copy() for row in self.board]
        
        if self.player_to_move == 0:  # Place vertical domino
            if not (0 <= row < self.size - 1 and 0 <= col < self.size and 
                   self.board[row][col] and self.board[row + 1][col]):
                raise ValueError("Invalid vertical domino placement")
            new_board[row][col] = False
            new_board[row + 1][col] = False
        else:  # Place horizontal domino
            if not (0 <= row < self.size and 0 <= col < self.size - 1 and 
                   self.board[row][col] and self.board[row][col + 1]):
                raise ValueError("Invalid horizontal domino placement")
            new_board[row][col] = False
            new_board[row][col + 1] = False
            
        return Domineering(self.size, new_board, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        # Game is over if current player has no legal moves
        return len(self.get_legal_actions()) == 0

    def get_result(self) -> Tuple[float, float]:
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # The player who CANNOT move loses (opposite of player_to_move)
        if self.player_to_move == 0:
            return (-1.0, 1.0)  # Player 1 won
        else:
            return (1.0, -1.0)  # Player 0 won

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        result = f"Turn: Player {self.player_to_move}"
        result += " (Vertical)\n" if self.player_to_move == 0 else " (Horizontal)\n"
        
        # Add column numbers with proper spacing for 2-digit numbers
        col_width = len(str(self.size - 1)) + 1
        result += " " * (col_width + 1)
        result += " ".join(str(i).ljust(col_width) for i in range(self.size)) + "\n"
        
        # Add board with row numbers
        for i, row in enumerate(self.board):
            result += str(i).ljust(col_width) + " "
            result += " ".join((".".ljust(col_width) if cell else "#".ljust(col_width)) 
                             for cell in row)
            result += "\n"
            
        return result
