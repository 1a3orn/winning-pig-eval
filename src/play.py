import asyncio
from play_base import play_single_game
from play_dataclasses import GameConfig, GameStats
from games.list import win_first_move_games
from save_results import save_results

# Constants
NUM_GAMES = 2
MODEL_NAMES = [
    #"claude-3-7-sonnet-20250219",
    "claude-3-5-haiku-20241022",
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
            print(f"\nPlaying: {config.num_games} games for {config.game_name}")
            for game_num in range(config.num_games):
                try:
                    stats = await play_single_game(config)
                    results.append(stats)
                except Exception as e:
                    print(f"Error in game {game_num + 1} for {config.game_name}: {str(e)}")
                    continue
        
        save_results(results)
    except Exception as e:
        print(f"Fatal error in main execution: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
