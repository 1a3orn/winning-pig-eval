from typing import Dict, List, Type
from dataclasses import dataclass
import json

from mcts.abstract_game import AbstractGameState

@dataclass
class GameConfig:
    # Just some string to identify the config
    run_name: str
    # The game class to play
    game_class: Type[AbstractGameState]
    # The LLM model to use
    model: str
    # The name of the game to play against
    game_name: str
    # The number of games to play
    num_games: int
    # The number of MCTS iterations to use
    mcts_iterations: int = 2000

@dataclass
class GameStats:
    # Configuration details we want to track
    run_name: str
    game_class_name: str  # Store class name instead of type
    model: str
    game_name: str
    mcts_iterations: int

    # Stats
    wins: int = 0
    losses: int = 0
    draws: int = 0
    invalid_moves: int = 0
    messages: List[Dict[str, str]] = None

    @classmethod
    def from_config(cls, config: GameConfig):
        return cls(
            run_name=config.run_name,
            game_class_name=config.game_class.__name__,  # Store the class name
            model=config.model,
            game_name=config.game_name,
            mcts_iterations=config.mcts_iterations,
        )

    def __post_init__(self):
        if self.messages is None:
            self.messages = []

    def to_dict(self) -> Dict:
        return {
            'wins': self.wins,
            'losses': self.losses,
            'draws': self.draws,
            'invalid_moves': self.invalid_moves,
            'messages': self.messages
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __json__(self):
        return self.to_dict()
    
    # Alternative approach using default encoder
    def default(self):
        return self.to_dict()

# Add this at the module level (after the class definition)
json.JSONEncoder.default = lambda self, obj: (obj.to_dict() if isinstance(obj, GameStats) else json.JSONEncoder.default(self, obj))
