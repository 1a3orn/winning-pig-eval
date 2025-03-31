import asyncio
import argparse
from play_base import play_single_game
from play_dataclasses import GameConfig, GameStats
from games.all_list import win_first_move_games, subset_games
from save_results import save_results

#"anthropic:claude-3-5-sonnet-20241022"
#"anthropic:claude-3-7-sonnet-20250219",
#"anthropic:claude-3-5-haiku-20241022",
#"deepseek:deepseek-chat",
#"deepseek:deepseek-reasoner",
#"openai:gpt-4o-2024-11-20",

async def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run games with specified AI model')
    parser.add_argument('--model_name', type=str, help='Name of the AI model to use, prefixed by the LLM provider (e.g. anthropic:claude-3-5-haiku-20241022)')
    parser.add_argument('--num_games', type=int, default=8, help='Number of games to play')
    args = parser.parse_args()

    configs = [
        GameConfig(
            run_name=f"{game_config['name']}_{args.model_name}_{game_config['mcts_iterations']}mcts",
            game_class=game_config['game_class'],
            model=args.model_name,
            game_name=game_config['name'],
            num_games=args.num_games,
            mcts_iterations=game_config['mcts_iterations']
        )
        for game_config in win_first_move_games
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
                            print(e)
                            continue
        
        save_results(results)
    except Exception as e:
        print(f"Fatal error in main execution: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
