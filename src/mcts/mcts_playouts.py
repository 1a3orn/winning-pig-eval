from mcts.mcts_playout import playout
from mcts.abstract_game import AbstractGameState

def test_game_wins(
        game: AbstractGameState,
        iters_first: int,
        iters_second: int,
        num_tests: int = 10,
        verbose: bool = False
    ):
    """
    Count wins for each player over multiple games with specified MCTS iters.
    
    Args:
        game: Game class to test
        iters: MCTS iterations per player
        num_tests: Number of games (default: 10)
        verbose: Print detailed results (default: False)
    """
    first_wins, second_wins = 0, 0
    for i in range(num_tests):
        result = playout(game(), iters_first, iters_second, verbose=verbose)
        if result[0] == 1.0 and result[1] == -1.0:
            first_wins += 1
        if result[0] == -1.0 and result[1] == 1.0:
            second_wins += 1
        if verbose:
            print(f"At game {i+1}: first wins {first_wins} of {num_tests}")
    
    return first_wins, second_wins