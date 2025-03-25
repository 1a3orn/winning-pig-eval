import os
from datetime import datetime
import json
import pandas as pd
from typing import List
from play_dataclasses import GameStats

def save_results(results: List[GameStats]):
    # Create results directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"{timestamp}_results"
    os.makedirs(results_dir, exist_ok=True)

    # Convert results to DataFrame
    df = pd.DataFrame([{
        'run_name': r.run_name,
        'game_class_name': r.game_class_name,
        'model': r.model,
        'game_name': r.game_name,
        'mcts_iterations': r.mcts_iterations,
        'wins': r.wins,
        'losses': r.losses,
        'draws': r.draws,
        'invalid_moves': r.invalid_moves
    } for r in results])

    # Save raw data
    df.to_csv(f"{results_dir}/raw_results.csv", index=False)
    
    # Save full data including messages to JSON
    with open(f"{results_dir}/full_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=lambda x: x.__dict__)

    # Save messages with context
    with open(f"{results_dir}/messages.txt", 'w') as f:
        for result in results:
            f.write(f"\nGame: {result.game_name}\n")
            f.write(f"Model: {result.model}\n")
            f.write(f"MCTS Iterations: {result.mcts_iterations}\n")
            f.write("-" * 50 + "\n")
            for msg in result.messages:
                f.write(f"Role: {msg['role']}\n")
                f.write(f"Content: {msg['content']}\n")
                f.write("-" * 30 + "\n")

    # Calculate aggregated statistics
    def aggregate_stats(df, group_col):
        grouped = df.groupby(group_col).agg({
            'wins': 'sum',
            'losses': 'sum',
            'draws': 'sum',
            'invalid_moves': 'sum'
        })
        
        stats = pd.DataFrame(index=grouped.index)
        total_games = grouped['wins'] + grouped['losses'] + grouped['draws']
        
        stats['Win Rate (%)'] = (grouped['wins'] / total_games * 100).round(2)
        stats['Draw Rate (%)'] = (grouped['draws'] / total_games * 100).round(2)
        stats['Loss Rate (%)'] = (grouped['losses'] / total_games * 100).round(2)
        stats['Invalid Move Rate (%)'] = (grouped['invalid_moves'] / total_games * 100).round(2)
        stats['Total Games'] = total_games
        
        return stats

    # Generate statistics
    game_stats = aggregate_stats(df, 'game_name')
    model_stats = aggregate_stats(df, 'model')

    # Print and save aggregated statistics
    with open(f"{results_dir}/aggregated_stats.txt", 'w') as f:
        f.write("Statistics by Game:\n")
        f.write("=" * 80 + "\n")
        f.write(game_stats.to_string(float_format='%.2f'))
        print("Statistics by Game:")
        print("=" * 80)
        print(game_stats.to_string(float_format='%.2f'))
        
        f.write("\n\nStatistics by Model:\n")
        f.write("=" * 80 + "\n")
        f.write(model_stats.to_string(float_format='%.2f'))
        print("\nStatistics by Model:")
        print("=" * 80)
        print(model_stats.to_string(float_format='%.2f')) 