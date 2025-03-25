from typing import List

from mcts.mcts_playouts import test_game_wins
from mcts.abstract_game import AbstractGameState

from games.list import win_first_move_games

def test_game_properties():
    verbose = False
    num_tests = 10  # Default number of tests for perfect play
    games = win_first_move_games

    for game_config in games:
        game, iters = game_config["game_class"], game_config["mcts_iterations"]
        game_name = game().get_name()
        print(f"\nTesting {game_name}")

        # Dumb player test:
        # - sometimes the second player wins if BOTH players are quite dumb
        f_wins, s_wins = test_game_wins(game, 25, 25, num_tests=num_tests, verbose=verbose)
        print(f" - Dumb player: {s_wins}/{num_tests} second player wins" +
              (" (PASSED)" if s_wins > 0 else " (FAILED)"))

        # Perfect play test:
        # - first player always wins, if both players think optimally
        f_wins, s_wins = test_game_wins(game, iters, iters, num_tests=num_tests, verbose=verbose)
        print(f" - Perfect play: {f_wins}/{num_tests} first player wins" + 
              (" (PASSED)" if f_wins == num_tests else " (FAILED)"))
        
 
if __name__ == "__main__":
    test_game_properties()
