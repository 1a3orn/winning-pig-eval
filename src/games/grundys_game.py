from typing import List, Tuple
from mcts.abstract_game import AbstractGameState

class GrundysGame(AbstractGameState):
    def __init__(self, heaps: List[int] = None, player_to_move: int = 0):
        # Initialize with default heap of 11 if no heaps provided
        self.heaps = heaps if heaps is not None else [11]
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Grundy's Game"

    def get_short_game_description(self) -> str:
        return """
A two-player game where players take turns splitting a heap into two unequal parts.
The game ends when no heap can be split further (only heaps of size 1 and 2 remain).
The last player able to make a valid move wins.
"""

    def get_detailed_rules(self) -> str:
        return """
Start condition: Game starts with a single heap of objects.

Rules:
- Two players alternate turns
- On your turn, you must choose one heap of size 3 or larger and split it into two unequal parts
- Heaps of size 1 or 2 cannot be split
- You can only split one heap per turn
- The game ends when no legal moves remain (all heaps are size 1 or 2)
- The last player who can make a legal move wins

Example:
- A heap of 5 can be split into:
  * 4 and 1
  * 3 and 2
- A heap of 3 can only be split into:
  * 2 and 1

To make a move, specify the heap index and the sizes of the two new heaps.
Format: 'heap_index:size1,size2' (e.g., '0:3,2' splits heap at index 0 into sizes 3 and 2)

Note that heaps will sorted after each move in descending order, so the largest heap is always at index 0.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal splits for all available heaps"""
        actions = []
        for heap_idx, heap_size in enumerate(self.heaps):
            if heap_size >= 3:
                # Generate all possible unequal splits
                for i in range(1, heap_size):
                    if i != heap_size - i:  # Ensure unequal parts
                        actions.append(f"{heap_idx}:{i},{heap_size-i}")
        return actions

    def take_action(self, action: str) -> 'GrundysGame':
        """Takes action in format 'heap_idx:size1,size2' and returns new state"""
        heap_idx_str, split_str = action.split(':')
        heap_idx = int(heap_idx_str)
        size1, size2 = map(int, split_str.split(','))
        
        if heap_idx >= len(self.heaps):
            raise ValueError("Invalid heap index")
        if size1 + size2 != self.heaps[heap_idx]:
            raise ValueError("Split sizes must sum to original heap size")
        if size1 == size2:
            raise ValueError("Split must be unequal")
        if size1 <= 0 or size2 <= 0:
            raise ValueError("Split sizes must be positive")

        # Create new heap list with the split
        new_heaps = self.heaps.copy()
        new_heaps.pop(heap_idx)
        new_heaps.extend([size1, size2])
        new_heaps.sort(reverse=True)  # Optional: keep heaps sorted for consistency

        return GrundysGame(new_heaps, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        """Returns True if no heap can be split further"""
        return all(heap_size <= 2 for heap_size in self.heaps)

    def get_result(self) -> Tuple[float, float]:
        """Returns (1, -1) if player 0 wins, (-1, 1) if player 1 wins"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # In normal play, the player who made the last move wins
        # So if it's player 1's turn, player 0 just won and vice versa
        if self.player_to_move == 1:
            return (1.0, -1.0)
        else:
            return (-1.0, 1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        heaps_str = ', '.join(str(h) for h in self.heaps)
        return f"Heaps: [{heaps_str}]\nPlayer {self.player_to_move}'s turn"
