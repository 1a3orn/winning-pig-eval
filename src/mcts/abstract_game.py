import abc
from typing import List, Tuple

class AbstractGameState(abc.ABC):
    """
    Abstract base class for games states
    for two-player, zero-sum games.

    Players divided into two groups: 0 and 1.
    """
    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Returns the name of the game.
        """
        pass

    @abc.abstractmethod
    def get_short_game_description(self) -> str:
        """
        Returns a short English-language description of the game.
        """
        pass

    @abc.abstractmethod
    def get_detailed_rules(self) -> str:
        """
        Returns a very detailed English-language description of the rules of the game.
        It should include everything.

        It should include the:
        - initial conditions of the game
        - rules of the game
        - win condition
        """
        pass

    @abc.abstractmethod
    def get_legal_actions(self) -> List[str]:
        """
        Returns a list of legal actions from the current state.
        Each action is a string.
        """
        pass

    @abc.abstractmethod
    def take_action(self, action: str) -> 'AbstractGameState':
        """
        Takes an action and returns the new state after applying the action.
        Any action must be one of the legal actions returned by get_legal_actions.
        """
        pass

    @abc.abstractmethod
    def is_terminal(self) -> bool:
        """
        Returns True if the current state is a terminal state, False otherwise. 
        A state is terminal if
        - one of the players has won the game
        - the game is a draw, i.e., there are no legal actions left
        """
        pass

    @abc.abstractmethod
    def get_result(self) -> Tuple[float, float]:
        """
        Returns the result of the game from the current state.
        The result is a tuple (player0_score, player1_score).
        Should be
        - (1, -1) if player 0 wins
        - (-1, 1) if player 1 wins
        """
        pass

    @abc.abstractmethod
    def get_player_to_move(self) -> int:
        """
        Returns the player whose turn it is to move.
        Should be 0 or 1.
        """
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the state,
        showing a string with the current state of the game and
        whose turn it is to move in an easy-to-read format.
        """
        pass