from typing import List, Tuple
import copy
from dataclasses import dataclass

from mcts.abstract_game import AbstractGameState

@dataclass
class WythofsNim(AbstractGameState):
    piles: List[int]  # Will always have exactly 2 piles
    player_to_move: int

    def __init__(self, piles: List[int] = None, player_to_move: int = 0):
        # Initialize with [5, 6] by default, or use provided piles
        self.piles = piles if piles is not None else [5, 6]
        if len(self.piles) != 2:
            raise ValueError("Wythof's Nim must have exactly 2 piles")
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Wythof's Nim"

    def get_short_game_description(self) -> str:
        return """
Players take turns removing tokens from two piles.
On your turn, you can either:
1. Remove any number of tokens from one pile, or
2. Remove an equal number of tokens from both piles.
The player who takes the last token WINS.
"""

    def get_detailed_rules(self) -> str:
        return """
Start condition: Two piles of tokens, traditionally labeled N and M.

Rules:
- Two players alternate turns
- On your turn, you have two types of moves:
  1. Remove any number of tokens from either pile
  2. Remove the same number of tokens from both piles
- You must remove at least one token on your turn
- The player who takes the last token WINS

To make a move, specify:
- For single pile moves: 'pile,tokens' (e.g., '0,3' removes 3 from pile 0)
- For both piles: 'both,tokens' (e.g., 'both,2' removes 2 from each pile)
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal moves"""
        actions = []
        # Single pile moves
        for pile in range(2):
            for tokens in range(1, self.piles[pile] + 1):
                actions.append(f"{pile},{tokens}")
        
        # Moves from both piles
        max_both = min(self.piles[0], self.piles[1])
        for tokens in range(1, max_both + 1):
            actions.append(f"both,{tokens}")
        
        return actions

    def take_action(self, action: str) -> 'WythofsNim':
        """Takes action and returns new state"""
        pile_or_both, tokens = action.split(',')
        tokens = int(tokens)
        
        new_piles = copy.deepcopy(self.piles)
        
        if pile_or_both == 'both':
            if tokens > min(self.piles):
                raise ValueError("Cannot remove more tokens than in either pile")
            new_piles[0] -= tokens
            new_piles[1] -= tokens
        else:
            pile = int(pile_or_both)
            if not (0 <= pile < 2):
                raise ValueError("Invalid pile number")
            if tokens > self.piles[pile]:
                raise ValueError("Cannot remove more tokens than in pile")
            new_piles[pile] -= tokens
            
        return WythofsNim(new_piles, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        """Returns True if game is over (no tokens remain)"""
        return sum(self.piles) == 0

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # The player who took the last token wins
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
        result += "Tokens in piles:\n"
        for i, tokens in enumerate(self.piles):
            result += f"Pile {i}: {tokens} tokens\n"
        return result
