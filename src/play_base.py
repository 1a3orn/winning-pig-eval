import os
from typing import Dict, List, Tuple

from llms.get_llm import get_llm
from mcts.abstract_game import AbstractGameState
from mcts.mcts_engine import MCTSEngine
from play_dataclasses import GameConfig, GameStats

async def play_single_game(config: GameConfig) -> GameStats:
    state = config.game_class()
    game_name = config.game_name
    
    # Initialize conversation
    messages = [
        {"role": "user", "content": create_system_prompt(state) + "\n" + create_turn_prompt(state)}
    ]
    move_history = []

    while not state.is_terminal():
        if state.get_player_to_move() == 0:  # LLM's turn (X)
            state, messages, invalid, move_history = await handle_llm_turn(
                config.model, state, messages, game_name, move_history
            )
            if invalid:
                return GameStats(
                    run_name=config.run_name,
                    game_class_name=config.game_class.__name__,
                    model=config.model,
                    game_name=game_name,
                    mcts_iterations=config.mcts_iterations,
                    wins=0, losses=0, draws=0,
                    invalid_moves=1,
                    messages=messages
                )
        else:  # MCTS turn (O)
            state, messages, move_history = handle_mcts_turn(
                state, messages, config.mcts_iterations, move_history
            )        
    result = state.get_result()
    wins = 1 if result[0] > 0 else 0
    losses = 1 if result[0] < 0 else 0
    draws = 1 if result[0] == 0 else 0

    #for message in messages:
    #    print("\n\n\n", message["role"])
    #    print(message["content"])
    
    return GameStats(
        run_name=config.run_name,
        game_class_name=config.game_class.__name__,
        model=config.model,
        game_name=game_name,
        mcts_iterations=config.mcts_iterations,
        wins=wins,
        losses=losses,
        draws=draws,
        invalid_moves=0,
        messages=messages
    )

def create_system_prompt(state: AbstractGameState) -> str:
    return f"""
You are playing a game of {state.get_name()}.
You move first. Your goal is to win the game.
Here are the detailed rules for the game:
--------------------------------
{state.get_detailed_rules()}
--------------------------------
The above were the detailed rules for the game.

Each turn, you will see the game state, and available moves.
Your goal is to win the game.
It is possible to guarantee a win only if you play perfectly FROM THE START.
Before moving, think through the strategic implications carefully.
After thinking, respond with your chosen move inside <move>...</move> XML tags.
"""

def create_turn_prompt(state: AbstractGameState, history: List[Tuple[str, AbstractGameState]] = None) -> str:
    if history is None:
        return f"""Current game state:
{str(state)}

You now have available the following moves: {', '.join(state.get_legal_actions())}

What is your next move? Think as long as you need to, then respond with your move in <move>...</move> tags."""

    prompt = ""
    # Only use the last 2 moves
    for i, (move, state_after) in list(enumerate(history))[-2::]:
        if i % 2 == 0:  # LLM's move
            prompt += f"You made move {move}\n"
            prompt += f"After you made this move, the state was:\n{str(state_after)}\n\n"
        else:  # Opponent's move
            prompt += f"Your opponent made move {move}\n"
            prompt += f"After he made this move, the state was:\n{str(state_after)}\n\n"
    
    prompt += f"You now have available the following moves: {', '.join(state.get_legal_actions())}\n\n"
    prompt += "What is your next move? Think as long as you need to, then respond with your move in <move>...</move> tags."
    return prompt

async def handle_llm_turn(
    model: str,
    state: AbstractGameState,
    messages: List[Dict[str, str]],
    game_name: str,
    move_history: List[Tuple[str, AbstractGameState]],
) -> Tuple[AbstractGameState, List[Dict[str, str]], int, List[Tuple[str, AbstractGameState]]]:
    try:
        response, move = await get_llm_move(model, state, messages)
        new_state = state.take_action(move)
        move_history.append((move, new_state))
        
        messages.append({"role": "assistant", "content": response})
        return new_state, messages, 0, move_history
    except (ValueError, IndexError):
        print(f"Invalid move in {game_name}")
        return state, messages, 1, move_history

def handle_mcts_turn(
    state: AbstractGameState,
    messages: List[Dict[str, str]],
    mcts_iterations: int,
    move_history: List[Tuple[str, AbstractGameState]]
) -> Tuple[AbstractGameState, List[Dict[str, str]], List[Tuple[str, AbstractGameState]]]:
    engine = MCTSEngine()
    move = engine.search(state, mcts_iterations)
    state_after_move = state.take_action(move)
    
    # Update history
    move_history.append((move, state_after_move))
    
    # Create new prompt with updated history
    if not state_after_move.is_terminal():
        message_content = create_turn_prompt(state_after_move, move_history)
    else:
        message_content = f"The opponent made move {move}. The game state is:\n{str(state_after_move)}\n\nGame over, they win."
    messages.append({"role": "user", "content": message_content})
    
    return state_after_move, messages, move_history

async def get_llm_move(
    model: str,
    state: AbstractGameState,
    messages: List[Dict[str, str]],
) -> str:

    llm = get_llm(model)
    response = await llm(messages)
    #print(response)
    
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