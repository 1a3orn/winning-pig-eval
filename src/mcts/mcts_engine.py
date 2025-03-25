import math
import random

from typing import Tuple

from mcts.abstract_game import AbstractGameState
from mcts.mcts_node import MCTSNode

class MCTSEngine:
    def __init__(self, exploration_constant: float = 1.0):
        self.exploration_constant = exploration_constant

    def search(self, state: AbstractGameState, iterations: int):
        root = MCTSNode(state)

        for _ in range(iterations):
            node = self.select(root)
            score = self.simulate(node.state)
            self.backpropagate(node, score)

        self.root = root

        # Print the total score for each node
        #for child in root.children:
        #   print(f"Node {child.state.get_player_to_move()} total score: {child.total_score}, visits: {child.visits}")

        return self.get_best_action(state.get_player_to_move(), root)

    def select(self, node: MCTSNode):
        while not node.state.is_terminal():
            if not node.is_fully_expanded():
                return self.expand(node)
            node = node.best_child(
                node.state.get_player_to_move(),
                self.exploration_constant
            )
        return node

    def expand(self, parent_node: MCTSNode):
        assert parent_node.children == []
        parent_node.children = [
            MCTSNode(parent_node.state.take_action(action), parent_node)
            for action
            in parent_node.state.get_legal_actions()
        ]
        return random.choice(parent_node.children)

    def simulate(self, state: AbstractGameState):
        while not state.is_terminal():
            action = random.choice(state.get_legal_actions())
            state = state.take_action(action)
        return state.get_result()

    def backpropagate(self, node: MCTSNode, score: Tuple[float, float]):
        while node is not None:
            node.visits += 1
            node.total_score[0] += score[0]
            node.total_score[1] += score[1]
            node = node.parent

    def get_best_action(self, perspective, root: MCTSNode):
        best_child = max(root.children, key=lambda child: child.visits)
        return root.state.get_legal_actions()[root.children.index(best_child)]
    