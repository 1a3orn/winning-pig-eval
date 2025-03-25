from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class Kayles(AbstractGameState):
    def __init__(self, pins: List[bool] = None, player_to_move: int = 0):
        # Initialize with 8 pins by default, or use provided pins
        # True represents a standing pin, False represents a removed pin
        self.pins = pins if pins is not None else [True] * 8
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Kayles"

    def get_short_game_description(self) -> str:
        return """
A game played with a row of pins. Players take turns removing either 1 pin or 2 adjacent pins.
The player who removes the last pin wins.
"""

    def get_detailed_rules(self) -> str:
        return f"""
Start condition: A row of standing pins.

Rules:
- Two players alternate turns
- On your turn, you must either:
  1. Remove any single standing pin
  2. Remove two adjacent standing pins
- You cannot remove two pins that are separated by an empty space
- The player who removes the last pin WINS
- If no pins remain and it's your turn, you've lost

To make a move, specify either:
- A single position to remove one pin (e.g., '3')
- Two adjacent positions to remove two pins (e.g., '3,4')
Positions are 0-indexed.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal moves in format 'pos' or 'pos1,pos2'"""
        actions = []
        # Single pin removals
        for i in range(len(self.pins)):
            if self.pins[i]:
                actions.append(str(i))
        
        # Adjacent pair removals
        for i in range(len(self.pins) - 1):
            if self.pins[i] and self.pins[i + 1]:
                actions.append(f"{i},{i+1}")
        
        return actions

    def take_action(self, action: str) -> 'Kayles':
        """Takes action and returns new state"""
        new_pins = self.pins.copy()
        
        if ',' in action:
            # Remove two adjacent pins
            pos1, pos2 = map(int, action.split(','))
            if not (0 <= pos1 < len(self.pins) and 0 <= pos2 < len(self.pins)):
                raise ValueError("Invalid positions")
            if abs(pos1 - pos2) != 1:
                raise ValueError("Pins must be adjacent")
            if not (self.pins[pos1] and self.pins[pos2]):
                raise ValueError("Pins must be standing")
            new_pins[pos1] = False
            new_pins[pos2] = False
        else:
            # Remove single pin
            pos = int(action)
            if not (0 <= pos < len(self.pins)):
                raise ValueError("Invalid position")
            if not self.pins[pos]:
                raise ValueError("Pin must be standing")
            new_pins[pos] = False

        return Kayles(new_pins, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        """Returns True if game is over (no pins remain)"""
        return not any(self.pins)

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # The player who just moved won (opposite of Nim)
        # If it's player 1's turn, player 0 just moved and won
        if self.player_to_move == 1:
            return (1.0, -1.0)
        # If it's player 0's turn, player 1 just moved and won
        else:
            return (-1.0, 1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        result = f"Turn: Player {self.player_to_move}\n"
        result += "Pins:  "
        for i, pin in enumerate(self.pins):
            result += "| " if pin else "  "
        result += "\n       "
        for i in range(len(self.pins)):
            result += f"{i} " if i < 10 else f"{i}"
        return result
