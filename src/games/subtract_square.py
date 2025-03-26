from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class SubtractSquare(AbstractGameState):
    """
    For details see https://en.wikipedia.org/wiki/Subtract_a_square
    - Probably invented by Richard A. Epstein  https://en.wikipedia.org/wiki/Richard_Arnold_Epstein
    - 

    """
    def __init__(self, number: int = 13, player_to_move: int = 0):
        self.number = number
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Subtract a Square"

    def get_short_game_description(self) -> str:
        return """
A two-player game where players take turns subtracting perfect squares from a number.
The player who reduces the number below 1 wins.
"""

    def get_detailed_rules(self) -> str:
        return """
Start condition: Game starts with some number.

Rules:
- Two players alternate turns
- On your turn, you must subtract a perfect square (1, 4, 9, 16, etc.) from the current number
- The square you subtract must be less than or equal to the current number
- The player who reduces the number below 1 to 0 wins
- You cannot subtract a square that is larger than the current number, i.e, make a negative number.

Example:
- If the current number is 13:
  * You can subtract 1 (leaving 12)
  * You can subtract 4 (leaving 9)
  * You can subtract 9 (leaving 4)
  * You cannot subtract 16 (too large)

To make a move, specify the square number to subtract (e.g., '9' to subtract 9)
Again, you win if you are the one who reduces the number to 0.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal squares that can be subtracted"""
        actions = []
        i = 1
        while i * i <= self.number:
            actions.append(str(i * i))
            i += 1
        return actions

    def take_action(self, action: str) -> 'SubtractSquare':
        """Takes action (a square number) and returns new state"""
        square = int(action)

        # Check not negative
        if square <= 0:
            raise ValueError("Cannot subtract a non-positive number")
        
        # Validate the move
        if square > self.number:
            raise ValueError("Cannot subtract a square larger than current number")
        
        # Check if it's actually a perfect square
        root = int(square ** 0.5)
        if root * root != square:
            raise ValueError("Must subtract a perfect square")

        return SubtractSquare(self.number - square, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        """Returns True if the number is less than 1"""
        return self.number < 1

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # The player who just moved (not player_to_move) is the winner
        if self.player_to_move == 1:
            return (1.0, -1.0)
        else:
            return (-1.0, 1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        return f"Current number: {self.number}\nPlayer {self.player_to_move}'s turn"
