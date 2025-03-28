from games.tic_tac_toe_uneven import TicTacToe3x4, TicTacToe4x3
from games.domineering import Domineering
from games.kayles import Kayles
from games.book_nim import BookNimEasy
from games.count_twenty_one import CountToTwentyOne
from games.coin_counter import CoinCounterGridState
from games.wythofs_nim import WythofsNim
from games.grundys_game import GrundysGame
from games.subtract_square import SubtractSquare
from games.turning_turtles import TurningTurtles
from games.connect_n import ConnectThree4x5, ConnectThree5x4

win_first_move_games = [
    { 
        "game_class": TicTacToe3x4, 
        "mcts_iterations": 8000,
        "name": "Tic Tac Toe (3x4, 3-in-a-row)",
        "category": "grid"
    },
    { 
        "game_class": TicTacToe4x3, 
        "mcts_iterations": 8000,
        "name": "Tic Tac Toe (4x3, 3-in-a-row)",
        "category": "grid"
    },
    {
        "game_class": CountToTwentyOne,
        "mcts_iterations": 80000,
        "name": "Count to Twenty-One",
        "category": "nim"
    },
    { 
        "game_class": Kayles, 
        "mcts_iterations": 10000,
        "name": "Kayles",
        "category": "nim"
    },
    { 
        "game_class": BookNimEasy, 
        "mcts_iterations": 5000, 
        "name": "Book Nim",
        "category": "nim"
    },
    {
        "game_class": WythofsNim,
        "mcts_iterations": 16000,
        "name": "Wythof's Nim",
        "category": "nim"
    },
    { 
        "game_class": Domineering, 
        "mcts_iterations": 1000,
        "name": "Domineering",
        "category": "grid"
    },
    {
        "game_class": CoinCounterGridState,
        "mcts_iterations": 8000,
        "name": "Coin Counter",
        "category": "grid"
    },
    {
        "game_class": GrundysGame,
        "mcts_iterations": 800,
        "name": "Grundy's Game",
        "category": "nim"
    },
    {
        "game_class": SubtractSquare,
        "mcts_iterations": 500,
        "name": "Subtract a Square",
        "category": "nim"
    },
    {
        "game_class": TurningTurtles,
        "mcts_iterations": 4000,
        "name": "Turning Turtles",
        "category": "nim"
    },
    {
        "game_class": ConnectThree4x5,
        "mcts_iterations": 1500,
        "name": "Connect 3 (4x5)",
        "category": "grid"
    },
    {
        "game_class": ConnectThree5x4,
        "mcts_iterations": 1500,
        "name": "Connect 3 (5x4)",
        "category": "grid"
    },   
]

# Make subset with just Book Nim, Coin Counter, and Connect 3 (4x5)
subset_games = [x for x in win_first_move_games if x['name'] in ["Book Nim", "Coin Counter", "Connect 3 (4x5)"]]