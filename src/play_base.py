import os
import json
from typing import Dict, List, Type, Tuple
import asyncio
from dataclasses import dataclass
from collections import defaultdict

from llms.anthropic import AnthropicAPI
from llms.deepseek import DeepseekAPI
from games.tic_tac_toe_uneven import (
    TicTacToeUnevenState,
    TicTacToe3x4,
    TicTacToe4x3,
    TicTacToe5x6with4inrow,
    TicTacToe6x5with4inrow
)
from mcts.mcts_playout import playout
from mcts.mcts_engine import MCTSEngine
from mcts.abstract_game import AbstractGameState

from llms.anthropic import AnthropicAPI
from llms.deepseek import DeepseekAPI

from play_dataclasses import GameConfig, GameStats

async def play_single_game(config: GameConfig) -> Tuple[int, int, int, int, List[Dict[str, str]]]:

    state = config.game_class()
    game_name = config.game_name
    invalid_moves = 0
    
    # Initialize conversation
    messages = [
        {"role": "system", "content": create_system_prompt(state)},
        {"role": "user", "content": create_turn_prompt(state, "")}
    ]

    while not state.is_terminal():
        if state.get_player_to_move() == 0:  # LLM's turn (X)
            state, messages, invalid = await handle_llm_turn(config.model, state, messages, game_name)
            if invalid:
                return (0, 0, 0, 1)
        else:  # MCTS turn (O)
            state, messages = handle_mcts_turn(state, messages, config.mcts_iterations)
            
    if not state.is_terminal():
        return (0, 0, 0, invalid_moves)
        
    result = state.get_result()
    wins = 1 if result[0] > 0 else 0
    losses = 1 if result[0] < 0 else 0
    draws = 1 if result[0] == 0 else 0

    for message in messages:
        print("\n\n\n", message["role"])
        print(message["content"])
    
    return GameStats(
        run_name=config.run_name,
        game_class_name=config.game_class.__name__,
        model=config.model,
        game_name=game_name,
        mcts_iterations=config.mcts_iterations,
        wins=wins,
        losses=losses,
        draws=draws,
        invalid_moves=invalid_moves,
        messages=messages
    )

def create_system_prompt(state: AbstractGameState) -> str:
    return f"""
You are playing a game of {state.get_name()}.
You are playing as X and will move first.
Here are the detailed rules for the game:
--------------------------------
{state.get_detailed_rules()}
--------------------------------
The above were the detailed rules of the game.

For each turn, you will see the board state and your available moves.
Please respond with your chosen move inside <move>...</move> XML tags.
Please think through the strategic implications carefully before making your move.
"""

def create_turn_prompt(state: AbstractGameState, to_prepend_next_message: str) -> str:
    return f"""{to_prepend_next_message if to_prepend_next_message else ''}
Current board state:
{str(state)}

Your available moves are: {', '.join(state.get_legal_actions())}

What is your next move? Think through the strategic implications carefully, then respond with your move in <move>...</move> tags."""

async def handle_llm_turn(
    model: str,
    state: AbstractGameState,
    messages: List[Dict[str, str]],
    game_name: str,
) -> Tuple[AbstractGameState, List[Dict[str, str]], int]:
    try:
        response, move = await get_llm_move(model, state, messages)
        new_state = state.take_action(move)
        messages.append({"role": "assistant", "content": response})
        return new_state, messages, 0
    except (ValueError, IndexError):
        print(f"Invalid move in {game_name} game {game_num}")
        return state, messages, 1

def handle_mcts_turn(
    state: AbstractGameState,
    messages: List[Dict[str, str]],
    mcts_iterations: int
) -> Tuple[AbstractGameState, List[Dict[str, str]]]:
    engine = MCTSEngine()
    result = engine.search(state, mcts_iterations)
    new_state = state.take_action(result)
    
    message_content = (
        create_turn_prompt(new_state, f"Your opponent played at position {result}.")
        if not new_state.is_terminal()
        else f"Your opponent played at position {result}. Game over."
    )
    messages.append({"role": "user", "content": message_content})
    
    return new_state, messages

async def get_llm_move(
    model: str,
    state: TicTacToeUnevenState,
    messages: List[Dict[str, str]],
) -> str:

    if 'claude' in model:
        llm = AnthropicAPI(os.getenv("ANTHROPIC_API_KEY"), temperature=0.6, model=model)
    else:
        llm = DeepseekAPI(os.getenv("DEEPSEEK_API_KEY"), temperature=0.6, model=model)

    response = await llm(messages)
    
    # Extract move from XML tags
    start_tag = "<move>"
    end_tag = "</move>"
    start_idx = response.find(start_tag) + len(start_tag)
    end_idx = response.find(end_tag)
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        raise ValueError("No valid move found in response")
    
    move = response[start_idx:end_idx].strip()
    if move not in state.get_legal_actions():
        raise ValueError(f"Invalid move: {move}")
    
    return response, move