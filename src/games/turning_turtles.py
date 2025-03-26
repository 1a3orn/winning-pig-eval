from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class TurningTurtles(AbstractGameState):
    def __init__(self, coins: List[bool] = None, player_to_move: int = 0):
        # True represents heads (H), False represents tails (T)
        if coins is None:
            self.coins = [True for i in range(5)] 
        else:
            self.coins = coins
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Turning Turtles"

    def get_short_game_description(self) -> str:
        return """
A game played with a row of coins. Players take turns flipping
a heads coin to tails, and optionally flipping one coin to its left either way. The player who
flips the last heads coin to tails wins.
"""

    def get_detailed_rules(self) -> str:
        return """
Start condition: A row of coins that can be heads (H) or tails (T).

Rules:
- Two players alternate turns
- On your turn, you must:
  1. Choose any coin showing heads and flip it to tails
  2. You may also flip ONE coin to the left of your chosen coin (optional)
- You cannot flip only a tails coin
- The player who flips the last heads coin to tails WINS
- If no heads remain and it's your turn, you've lost

To make a move, specify either:
- A single position to flip from heads to tails (e.g., '3')
- Two positions where the right one is heads and will be flipped to tails,
  and the left one will be flipped either way (e.g., '2,3')
Positions are 0-indexed.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal moves in format 'pos' or 'leftpos,rightpos'"""
        actions = []
        # Single flips (H->T only)
        for i in range(len(self.coins)):
            if self.coins[i]:  # if heads
                actions.append(str(i))
        
        # Double flips (right coin must be H, left coin can be either)
        for right in range(len(self.coins)):
            if self.coins[right]:  # if right coin is heads
                for left in range(right):  # any coin to the left
                    actions.append(f"{left},{right}")
        
        return actions

    def take_action(self, action: str) -> 'TurningTurtles':
        """Takes action and returns new state"""
        new_coins = self.coins.copy()
        
        if ',' in action:
            # Flip two coins
            left, right = map(int, action.split(','))
            if not (0 <= left < len(self.coins) and 0 <= right < len(self.coins)):
                raise ValueError("Invalid positions")
            if left >= right:
                raise ValueError("Left position must be less than right position")
            if not self.coins[right]:
                raise ValueError("Right coin must be heads")
            new_coins[left] = not new_coins[left]  # flip left coin
            new_coins[right] = False  # flip right coin to tails
        else:
            # Flip single coin from heads to tails
            pos = int(action)
            if not (0 <= pos < len(self.coins)):
                raise ValueError("Invalid position")
            if not self.coins[pos]:
                raise ValueError("Coin must be heads")
            new_coins[pos] = False

        return TurningTurtles(new_coins, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        """Returns True if game is over (no heads remain)"""
        return not any(self.coins)

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # The player who just moved won
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
        result += "Coins: "
        for coin in self.coins:
            result += "H " if coin else "T "
        result += "\n       "
        for i in range(len(self.coins)):
            result += f"{i} " if i < 10 else f"{i}"
        return result
