from typing import List, Tuple, Optional
from mcts.abstract_game import AbstractGameState

class ConnectN(AbstractGameState):
    def __init__(self, rows: int, cols: int, n_to_win: int, board: List[List[str]] = None, player_to_move: int = 0):
        self.rows = rows
        self.cols = cols
        self.n_to_win = n_to_win
        # Initialize empty board if none provided
        self.board = [row.copy() for row in board] if board is not None else [[' ' for _ in range(cols)] for _ in range(rows)]
        self.player_to_move = player_to_move
        self.symbols = ['X', 'O']

    def get_name(self) -> str:
        return f"Connect{self.n_to_win}, on a {self.rows}x{self.cols} board"

    def get_short_game_description(self) -> str:
        return f"""
A {self.rows}x{self.cols} board game where players take turns dropping {self.symbols[0]} or {self.symbols[1]} into columns.
Connect {self.n_to_win} in a line (horizontally, vertically, or diagonally) to win.
The line must be uninterrupted.
"""

    def get_detailed_rules(self) -> str:
        return f"""
Start condition: An empty {self.rows}x{self.cols} board.
It has {self.rows} rows and {self.cols} columns.

Rules:
- Two players alternate turns
- Player 0 uses '{self.symbols[0]}', Player 1 uses '{self.symbols[1]}'
- On your turn, drop your symbol in any non-full column
- Pieces stack from bottom to top in each column
- First to connect {self.n_to_win} of their symbols in a continuous line wins
- The line must be uninterrupted.
- The line may be horizontal, vertical, or diagonal.
- If the board fills up with no winner, it's a draw

To make a move, specify the column number from column 0 to column {self.cols-1}
You will be playing with {self.symbols[self.player_to_move]}.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal columns (those not full)"""
        return [str(col) for col in range(self.cols) if self.board[0][col] == ' ']

    def take_action(self, action: str) -> 'ConnectN':
        """Takes action and returns new state"""
        try:
            col = int(action)
        except ValueError:
            raise ValueError("Invalid action: must be a string representing an integer")
        if not (0 <= col < self.cols):
            raise ValueError("Invalid column")
        if self.board[0][col] != ' ':
            raise ValueError("Column is full")

        # Create a deep copy of the board
        new_board = [row[:] for row in self.board]
        row = self.rows - 1
        while row >= 0 and new_board[row][col] != ' ':
            row -= 1
        # Add safety check
        if row < 0:
            raise ValueError("Column is full")
        new_board[row][col] = self.symbols[self.player_to_move]

        return ConnectN(self.rows, self.cols, self.n_to_win, new_board, 1 - self.player_to_move)

    def _check_winner(self) -> Optional[int]:
        """Returns winning player (0 or 1) or None if no winner"""
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - self.n_to_win + 1):
                if self.board[row][col] != ' ':
                    if all(self.board[row][col+i] == self.board[row][col] for i in range(self.n_to_win)):
                        return 0 if self.board[row][col] == self.symbols[0] else 1

        # Check vertical
        for row in range(self.rows - self.n_to_win + 1):
            for col in range(self.cols):
                if self.board[row][col] != ' ':
                    if all(self.board[row+i][col] == self.board[row][col] for i in range(self.n_to_win)):
                        return 0 if self.board[row][col] == self.symbols[0] else 1

        # Check diagonal (top-left to bottom-right)
        for row in range(self.rows - self.n_to_win + 1):
            for col in range(self.cols - self.n_to_win + 1):
                if self.board[row][col] != ' ':
                    if all(self.board[row+i][col+i] == self.board[row][col] for i in range(self.n_to_win)):
                        return 0 if self.board[row][col] == self.symbols[0] else 1

        # Check diagonal (top-right to bottom-left)
        for row in range(self.rows - self.n_to_win + 1):
            for col in range(self.n_to_win - 1, self.cols):
                if self.board[row][col] != ' ':
                    if all(self.board[row+i][col-i] == self.board[row][col] for i in range(self.n_to_win)):
                        return 0 if self.board[row][col] == self.symbols[0] else 1

        return None

    def is_terminal(self) -> bool:
        """Returns True if game is over (winner or draw)"""
        return self._check_winner() is not None or len(self.get_legal_actions()) == 0

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins, (0, 0) for draw"""
        winner = self._check_winner()
        if winner is None:
            return (0.0, 0.0)  # Draw
        elif winner == 0:
            return (1.0, -1.0)
        else:
            return (-1.0, 1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        result = f"Turn: Player {self.player_to_move} ({self.symbols[self.player_to_move]})\n"
        for row in self.board:
            result += '|' + '|'.join(row) + '|\n'
        result += '-' * (self.cols * 2 + 1) + '\n'
        result += ' ' + ' '.join(str(i) for i in range(self.cols))
        return result


class ConnectThree4x5(ConnectN):
    def __init__(self, board: List[List[str]] = None, player_to_move: int = 0, rows: int = 4, cols: int = 5, n_to_win: int = 3):
        super().__init__(rows=rows, cols=cols, n_to_win=n_to_win, board=board, player_to_move=player_to_move)


class ConnectThree5x4(ConnectN):
    def __init__(self, board: List[List[str]] = None, player_to_move: int = 0, rows: int = 5, cols: int = 4, n_to_win: int = 3):
        super().__init__(rows=rows, cols=cols, n_to_win=n_to_win, board=board, player_to_move=player_to_move)
