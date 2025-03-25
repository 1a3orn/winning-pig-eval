import time
import threading
from typing import Tuple

from mcts.abstract_game import AbstractGameState
from mcts.mcts_engine import MCTSEngine

class IterationTimeout(Exception):
    pass

def playout(state: AbstractGameState, i1: int, i2: int, iteration_timeout: float = 30.0, verbose: bool = False) -> Tuple[int, int]:
    iters = 0
    start_time = time.time()
    
    while not state.is_terminal():
        iterations = i1 if state.get_player_to_move() == 0 else i2
        
        # 1. First, we create the "player" (MCTSEngine) who will think about the move
        engine = MCTSEngine()
        result, exception = None, None
        
        # 2. Then, we create the worker thread that will search for the best move
        def search_worker():
            nonlocal result, exception
            try:
                result = engine.search(state, iterations)
            except Exception as e:
                exception = e
        
        # 3. Create and start the worker thread, with 
        #    a timeout of 10 seconds
        thread = threading.Thread(target=search_worker)
        thread.daemon = True
        thread.start()
        thread.join(timeout=iteration_timeout)
        
        if thread.is_alive():
            # If thread is still running after timeout
            raise TimeoutError("Single iteration took too long")
            
        if exception:
            # Re-raise any exception that occurred in the thread
            raise exception
            
        if result is None:
            raise RuntimeError("Search failed to produce a result")
            
        action = result
        state = state.take_action(action)
        iters += 1

        # Print what end-game state looks like
        if verbose:
            print(str(state))
        
        if iters > 90:
            raise TimeoutError("Too many iterations")
        if time.time() - start_time > 1000:
            print("Too much time")
            raise TimeoutError("Too much time spent in playout")

    if verbose:
        print(f"Total iterations: {iters}")

    return state.get_result()