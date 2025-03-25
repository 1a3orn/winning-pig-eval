from typing import List, Tuple
import copy
from dataclasses import dataclass

from mcts.abstract_game import AbstractGameState

@dataclass
class BookNim(AbstractGameState):
    shelves: List[int]
    player_to_move: int

    def __init__(self, shelves: List[int] = None, player_to_move: int = 0):
        # Initialize with 1, 3, 4 books by default, or use provided shelves
        self.shelves = shelves if shelves is not None else [3, 4, 5]
        self.player_to_move = player_to_move

    def get_name(self) -> str:
        return "Book Nim"

    def get_short_game_description(self) -> str:
        return """
Players take turns removing any number of books from a single shelf.
The game starts with three shelves containing various numbers of books.
The player who takes the last book loses.
"""

    def get_detailed_rules(self) -> str:
        return """
Start condition: Three shelves of books, with various numbers of books on each shelf.

Rules:
- Two players alternate turns
- On your turn, you must remove at least one book from exactly one shelf
- You may remove any number of books from your chosen shelf, up to all books on that shelf
- You cannot remove books from multiple shelves in a single turn
- The player who takes the last book loses
- If no books remain and you cannot make a move, you lose

To make a move, specify the shelf number and number of books to remove.
For example, to remove 2 books from shelf 1, specify the move '1,2'.
"""

    def get_legal_actions(self) -> List[str]:
        """Returns list of legal moves in format 'shelf,books_to_remove'"""
        actions = []
        for shelf in range(len(self.shelves)):
            for books in range(1, self.shelves[shelf] + 1):
                actions.append(f"{shelf},{books}")
        return actions

    def take_action(self, action: str) -> 'BookNim':
        """Takes action in format 'shelf,books_to_remove' and returns new state"""
        shelf, books = map(int, action.split(','))
        if not (0 <= shelf < len(self.shelves)):
            raise ValueError("Invalid shelf")
        if not (1 <= books <= self.shelves[shelf]):
            raise ValueError("Invalid number of books")

        new_shelves = copy.deepcopy(self.shelves)
        new_shelves[shelf] -= books
        return BookNim(new_shelves, 1 - self.player_to_move)

    def is_terminal(self) -> bool:
        """Returns True if game is over (no books remain)"""
        return sum(self.shelves) == 0

    def get_result(self) -> Tuple[float, float]:
        """Returns (-1, 1) if player 0 loses, (1, -1) if player 1 loses"""
        if not self.is_terminal():
            raise ValueError("Game is not over")
        
        # The player who takes the last book loses
        # If it's player 1's turn, player 0 just moved and lost
        if self.player_to_move == 1:
            return (-1.0, 1.0)
        # If it's player 0's turn, player 1 just moved and lost
        else:
            return (1.0, -1.0)

    def get_player_to_move(self) -> int:
        return self.player_to_move

    def __str__(self) -> str:
        """Returns string representation of the game state"""
        result = f"Turn: Player {self.player_to_move}\n"
        result += "Books on shelves:\n"
        for i, books in enumerate(self.shelves):
            result += f"Shelf {i}: {books} books\n"
        return result

class BookNimEasy(BookNim):
    def __init__(self, shelves: List[int] = None, player_to_move: int = 0):
        # Initialize with 1, 3, 4 books by default
        super().__init__(shelves if shelves is not None else [1, 3, 4], player_to_move)

    def get_name(self) -> str:
        return "Book Nim"

class BookNimHard(BookNim):
    def __init__(self, shelves: List[int] = None, player_to_move: int = 0):
        # Initialize with 2, 4, 5 books by default
        super().__init__(shelves if shelves is not None else [2, 4, 5], player_to_move)
