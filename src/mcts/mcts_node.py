import math
import random

from mcts.abstract_game import AbstractGameState

class MCTSNode:
    def __init__(self, state: AbstractGameState, parent: 'MCTSNode' = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_score = [0, 0]
        self.is_terminal = state.is_terminal()

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_actions())

    def best_child(self, perspective, exploration_constant: float = 1.0):
        return max(self.children, key=lambda child: child.ucb1_score(perspective, exploration_constant))

    def ucb1_score(self, perspective, exploration_constant: float):
        if self.visits == 0:
            return float('inf')
        exploitation_term = self.total_score[perspective] / self.visits
        exploration_term = exploration_constant * math.sqrt(math.log(self.parent.visits) / (1.0 + self.visits))
        return exploitation_term + exploration_term
    
    def percent_terminal_leafs(self):
        if len(self.children) > 0:
            total = 0
            is_terminal = 0
            for child in self.children:
                total_s, is_terminal_s = child.percent_terminal_leafs()
                total += total_s
                is_terminal += is_terminal_s
            return total, is_terminal
        else:
            return 1, 1 if self.is_terminal else 0