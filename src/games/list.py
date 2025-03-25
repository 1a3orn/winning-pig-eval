from games.tic_tac_toe_uneven import TicTacToe3x4
from games.domineering import Domineering
from games.kayles import Kayles
from games.book_nim import BookNimEasy


win_first_move_games = [
    { 
        "game_class": TicTacToe3x4, 
        "mcts_iterations": 4000,
        "name": "Tic Tac Toe (3x4, 3-in-a-row)"
    },
    { 
        "game_class": Domineering, 
        "mcts_iterations": 1000,
        "name": "Domineering"
    },
    { 
        "game_class": Kayles, 
        "mcts_iterations": 10000,
        "name": "Kayles"
    },
    { 
        "game_class": BookNimEasy, 
        "mcts_iterations": 5000, 
        "name": "Book Nim"
    },
]