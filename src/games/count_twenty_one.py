from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class CountToTwentyOne(AbstractGameState):
    def __init__(self, current_number: int = 0, player_to_move: int = 0):
        self.current_number = current_number
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Count to Twenty-One"

    def get_short_game_description(self) -> str:
        return """
Players take turns counting up from 1 to 21. On your turn, you must count 1, 2, or 3 
consecutive numbers. The player who says 21 wins.
"""

    def get_detailed_rules(self) -> str:
        return """
Start condition: Game starts at 0.

Rules:
- Two players alternate turns
- On your turn, you must count 1, 2, or 3 consecutive numbers
- Numbers must be counted in sequence
- The player who says 21 WINS

Example turn:
- If current number is 5, you can say:
  * "6" (count 1 number)
  * "6, 7" (count 2 numbers)
  * "6, 7, 8" (count 3 numbers)

To make a move, specify which number you want to count to: '6', '7', or '8' and so on.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of next possible numbers that can be counted.
        For example, if current_number is 5, returns ['6', '7', '8']"""
        actions = []
        for count in range(self.current_number + 1, self.current_number + 4):
            if count <= 21:
                actions.append(str(count))
        return actions

    def take_action(self, action: str) -> 'CountToTwentyOne':
        """Takes action and returns new state.
        Action should be the target number to count to."""
        count = int(action)
        if count <= self.current_number:
            raise ValueError("Must count higher than current number")
        if count > 21:
            raise ValueError("Cannot count beyond 21")
        if count - self.current_number > 3:
            raise ValueError("Cannot count more than 3 numbers")
        return CountToTwentyOne(
            count,
            1 - self.player_to_move
        )

    def is_terminal(self) -> bool:
        """Returns True if game is reached 21"""
        return self.current_number == 21

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # player 1's turn = player 0 just moved and won
        if self.player_to_move == 1:
            return (1.0, -1.0)
        # player 0's turn = player 1 just moved and won
        else:
            return (-1.0, 1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        return f"Current number: {self.current_number}\nPlayer {self.player_to_move}'s turn"
