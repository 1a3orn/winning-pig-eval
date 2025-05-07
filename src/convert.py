import pandas as pd
import sys

def analyze_game_results(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Calculate percentages for each game
    game_stats = df.groupby('game_name').agg({
        'wins': 'sum',
        'losses': 'sum',
        'draws': 'sum',
        'invalid_moves': 'sum'
    })
    
    # Calculate total games for each game
    game_stats['total_games'] = game_stats.sum(axis=1)
    
    # Calculate percentages for each game
    for col in ['wins', 'losses', 'draws', 'invalid_moves']:
        game_stats[f'{col}_rate'] = (game_stats[col] / game_stats['total_games'] * 100).round(1)
    
    # Calculate overall model statistics
    model_stats = df.agg({
        'wins': 'sum',
        'losses': 'sum',
        'draws': 'sum',
        'invalid_moves': 'sum'
    })
    
    total_games = model_stats.sum()
    model_stats = model_stats / total_games * 100
    
    # Print results
    print("\nGame-specific Statistics:")
    print("=" * 80)
    print(game_stats[['wins_rate', 'losses_rate', 'draws_rate', 'invalid_moves_rate', 'total_games']].to_string())
    
    print("\nOverall Model Statistics:")
    print("=" * 80)
    print(f"Win Rate: {model_stats['wins']:.1f}%")
    print(f"Loss Rate: {model_stats['losses']:.1f}%")
    print(f"Draw Rate: {model_stats['draws']:.1f}%")
    print(f"Invalid Move Rate: {model_stats['invalid_moves']:.1f}%")
    print(f"Total Games: {total_games}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    analyze_game_results(csv_path)