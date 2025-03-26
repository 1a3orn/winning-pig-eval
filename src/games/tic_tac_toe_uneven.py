from typing import List, Tuple
import copy
from dataclasses import dataclass

from mcts.abstract_game import AbstractGameState

@dataclass
class TicTacToeUnevenState(AbstractGameState):
    board: List[List[str]]
    player_to_move: int

    def __init__(
            self,
            board: List[List[str]] = None,
            player_to_move: int = 0,
            num_rows: int = 3,
            num_cols: int = 4,
            num_in_a_row: int = 3
        ):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_in_a_row = num_in_a_row
        self.board = board if board is not None else [['' for _ in range(num_cols)] for _ in range(num_rows)]
        self.player_to_move = player_to_move

    def get_short_game_description(self) -> str:
        return f"""
Two players alternate turns, placing 'X' and 'O' alternately on empty spots on a grid with {self.num_rows} rows and {self.num_cols} columns.
That is, they place their symbol on a spot with row index {row} and column index {col}, where 0 <= {row} <= {self.num_rows - 1} and 0 <= {col} <= {self.num_cols - 1}.
A player wins by getting {self.num_in_a_row} of their symbols in a row.
Winning rows must be contiguous lines. Lines may be horizontal, vertical, or diagonal.
"""

    def get_name(self) -> str:
        return f"Modified Tic Tac Toe ({self.num_rows} x {self.num_cols}, {self.num_in_a_row}-in-a-row)"

    def get_detailed_rules(self) -> str:
        return f"""\
Start condition: An empty {self.num_rows} x {self.num_cols} grid.
The grid has {self.num_rows} rows and {self.num_cols} columns.
The grid is indexed from 0,0 in the top-left corner to {self.num_rows-1},{self.num_cols-1} in the bottom-right corner.

Rules:
- Two players alternate turns.
- On each turn, a player places their symbol ('X' or 'O') on an empty spot on the grid.
- The first player uses 'X', the second player uses 'O'.
- A player wins by getting {self.num_in_a_row} of their symbols in a contiguous line.
- The {self.num_in_a_row}-in-a-line can be horizontal, vertical, or diagonal.
- If no player achieves {self.num_in_a_row}-in-a-line and the board is full, the game is a draw.

To make a move, specify the 0-indexed row and column of the spot to place your symbol.
For example, to move in the 0th row and the 2nd column, specify the move '0,2'.
Or, to move in the 1st row and the 0th column, specify the move '1,0'.
The top-left corner of the grid is at position 0,0.
The bottom-right corner is at position {self.num_rows-1},{self.num_cols-1}.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal moves in format 'row,col'"""
        actions = []
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.board[row][col] == '':
                    actions.append(f"{row},{col}")
        return actions

    def take_action(self, action: str) -> 'TicTacToeUnevenState':
        """Takes action in format 'row,col' and returns new state"""
        row, col = map(int, action.split(','))
        if not (0 <= row < self.num_rows and 0 <= col < self.num_cols):
            raise ValueError("Invalid position")
        if self.board[row][col] != '':
            raise ValueError("Position already occupied")

        new_board = copy.deepcopy(self.board)
        new_board[row][col] = 'X' if self.player_to_move == 0 else 'O'
        return TicTacToeUnevenState(
            new_board,
            player_to_move=1 - self.player_to_move,
            num_rows=self.num_rows,
            num_cols=self.num_cols,
            num_in_a_row=self.num_in_a_row
        )

    def _check_win(self) -> bool:
        """Check if current state is a win for either player"""
        # Check rows
        for row in range(self.num_rows):
            for col in range(self.num_cols - self.num_in_a_row + 1):
                if (self.board[row][col] != ''):
                    # Check if there are {self.num_in_a_row} consecutive symbols in the row
                    # in the same direction
                    valid = all([
                        self.board[row][col+i] == self.board[row][col]
                        for i in range(self.num_in_a_row)
                    ])
                    if valid:
                        return True

        # Check columns
        for row in range(self.num_rows - self.num_in_a_row + 1):
            for col in range(self.num_cols):
                if (self.board[row][col] != ''):
                    valid = all([
                        self.board[row+i][col] == self.board[row][col]
                        for i in range(self.num_in_a_row)
                    ])
                    if valid:
                        return True

        # Check diagonals
        # Down-right diagonals
        for row in range(self.num_rows - self.num_in_a_row + 1):
            for col in range(self.num_cols - self.num_in_a_row + 1):
                if (self.board[row][col] != ''):
                    valid = all([
                        self.board[row+i][col+i] == self.board[row][col]
                        for i in range(self.num_in_a_row)
                    ])
                    if valid:
                        return True

        # Down-left diagonals
        for row in range(self.num_rows - self.num_in_a_row + 1):
            for col in range(self.num_cols - 1, self.num_in_a_row - 2, -1):
                if (self.board[row][col] != ''):
                    valid = all([
                        self.board[row+i][col-i] == self.board[row][col]
                        for i in range(self.num_in_a_row)
                    ])
                    if valid:
                        return True

        return False

    def is_terminal(self) -> bool:
        """Returns True if game is over"""
        if self._check_win():
            return True
        return len(self.get_legal_actions()) == 0

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        if self._check_win():
            # If it's player 1's turn, player 0 just moved and won
            if self.player_to_move == 1:
                return (1.0, -1.0)
            # If it's player 0's turn, player 1 just moved and won
            else:
                return (-1.0, 1.0)
        
        # If no winner but game is terminal, it's a draw
        return (0.0, 0.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        result = f"Turn: {'X' if self.player_to_move == 0 else 'O'}\n"
        # Add column numbers
        result += "Board:\n"
        result += "  " + "   ".join(str(i) for i in range(self.num_cols)) + "\n"
        for row in range(self.num_rows):
            # Add row number
            result += f"{row} "
            result += " | ".join(cell if cell != '' else ' ' for cell in self.board[row])
            if row < self.num_rows - 1:
                result += "\n" + "  " + "-" * (self.num_cols * 4 - 2) + "\n"
        return result

# Note that wikipedia specifies that all the following
# (i.e, 3x4 or 4x3 with 3-in-a-row, 5x6 or 6x5 with 4-in-a-row)
# are first-to-move win games

class TicTacToe3x4(TicTacToeUnevenState):
    """
    Tic Tac Toe on a 3x4 grid with 3-in-a-row
    """
    def __init__(self, board: List[List[str]] = None, player_to_move: int = 0):
        super().__init__(board, player_to_move, num_rows=3, num_cols=4, num_in_a_row=3)

class TicTacToe4x3(TicTacToeUnevenState):
    """
    Tic Tac Toe on a 4x3 grid with 3-in-a-row
    """
    def __init__(self, board: List[List[str]] = None, player_to_move: int = 0):
        super().__init__(board, player_to_move, num_rows=4, num_cols=3, num_in_a_row=3)

class TicTacToe6x5with4inrow(TicTacToeUnevenState):
    """
    Tic Tac Toe on a 6x5 grid with 4-in-a-row
    """
    def __init__(self, board: List[List[str]] = None, player_to_move: int = 0):
        super().__init__(board, player_to_move, num_rows=6, num_cols=5, num_in_a_row=4)

class TicTacToe5x6with4inrow(TicTacToeUnevenState):
    """
    Tic Tac Toe on a 5x6 grid with 4-in-a-row
    """
    def __init__(self, board: List[List[str]] = None, player_to_move: int = 0):
        super().__init__(board, player_to_move, num_rows=5, num_cols=6, num_in_a_row=4)
