import asyncio
from play_base import play_single_game
from play_dataclasses import GameConfig, GameStats
from games.all_list import win_first_move_games, subset_games
from save_results import save_results

# Constants
NUM_GAMES = 8
MODEL_NAMES = [
    #"claude-3-7-sonnet-20250219",
    #"claude-3-5-haiku-20241022",
    #"claude-3-7-sonnet-20250219",
    #"gemini-2.5-pro-exp-03-25",
    #"deepseek-chat",
    #"deepseek-reasoner",
    #"gpt-4o-2024-11-20",
    #"gpt-4.5-preview-2025-02-27",
    #"o3-mini-2025-01-31",
    #"o1-2024-12-17",
    "claude-3-5-sonnet-20241022"
    #"o3-mini-2025-01-31",
    # "gpt-4o-2024-11-20",
    #"gpt-4o-mini-2024-07-18",
    #"human_terminal",
]

async def main():
    # Create game configs as cross product of game classes + models
    configs = [
        GameConfig(
            run_name=f"{game_config['name']}_{model}_{game_config['mcts_iterations']}mcts",
            game_class=game_config['game_class'],
            model=model,
            game_name=game_config['name'],
            num_games=NUM_GAMES,
            mcts_iterations=game_config['mcts_iterations']
        )
        for game_config in win_first_move_games
        for model in MODEL_NAMES
    ]
    
    try:
        results = []
        for config in configs:
            print(f"{config.num_games} games {config.game_name} with {config.model}")
            for game_num in range(config.num_games):
                attempts = 0
                max_attempts = 3
                while attempts < max_attempts:
                    try:
                        print(f"Game {game_num + 1} of {config.num_games} (Attempt {attempts + 1}/{max_attempts})")
                        stats = await play_single_game(config)
                        results.append(stats)
                        break  # Success - exit retry loop
                    except Exception as e:
                        attempts += 1
                        if attempts == max_attempts:
                            print(f"Failed all {max_attempts} attempts for game {game_num + 1} of {config.game_name}: {str(e)}")
                        else:
                            print(f"Attempt {attempts} failed for game {game_num + 1} of {config.game_name}: {str(e)}")
                            continue
        
        save_results(results)
    except Exception as e:
        print(f"Fatal error in main execution: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
