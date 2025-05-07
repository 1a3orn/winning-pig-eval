## Intro
**PigBench**

LLMs are notoriously bad at tic-tac-toe.  But what about other two-player perfect information games (PIGs)?

I test several LLMs against 13 two-player perfect-information-games where, with perfect play, the first player can always win. As it turns out, most LLMs do poorly against this task.

## To Run 

To run

python src/play.py --model_name [model_name] --num_games [num_games]

See src/llms/get_llm.py for how to add models and how to add model names.

I've verified that the first player can always win both by running the games with MCTS with both players rollouts set to be very high, and also by winning myself against the MCTS. Set model_name to be human_terminal to test it out yourself.

## Stats

Performance of some selected models (did not test against reasoning models from OpenAI due to expense):
![performance of models](/image1.png)

Per game performance from Gemini 2.5 pro 05/06, with an average win rate of ~70%:

```
Game-specific Statistics:
================================================================================
                               wins_rate  losses_rate  draws_rate  invalid_moves_rate  total_games
game_name                                                                                         
Book Nim                           100.0          0.0         0.0                 0.0            8
Coin Counter                        12.5         50.0         0.0                37.5            8
Connect 3 (4x5)                     50.0         50.0         0.0                 0.0            8
Connect 3 (5x4)                     25.0         75.0         0.0                 0.0            8
Count to Twenty-One                100.0          0.0         0.0                 0.0            8
Domineering                         12.5         87.5         0.0                 0.0            8
Grundy's Game                      100.0          0.0         0.0                 0.0            8
Kayles                             100.0          0.0         0.0                 0.0            8
Subtract a Square                  100.0          0.0         0.0                 0.0            8
Tic Tac Toe (3x4, 3-in-a-row)       62.5         25.0        12.5                 0.0            8
Tic Tac Toe (4x3, 3-in-a-row)       87.5         12.5         0.0                 0.0            8
Turning Turtles                     62.5         37.5         0.0                 0.0            8
Wythof's Nim                       100.0          0.0         0.0                 0.0            8

Overall Model Statistics:
================================================================================
Win Rate: 70.2%
Loss Rate: 26.0%
Draw Rate: 1.0%
Invalid Move Rate: 2.9%
Total Games: 104```


Per game performance from Gemini 2.5 Experimental, with an average win rate ~70%:
```
Game-specific Statistics:
================================================================================
                               wins_rate  losses_rate  draws_rate  invalid_moves_rate  total_games
game_name                                                                                         
Book Nim                           100.0          0.0         0.0                 0.0            8
Coin Counter                         0.0        100.0         0.0                 0.0            8
Connect 3 (4x5)                     75.0         25.0         0.0                 0.0            8
Connect 3 (5x4)                      0.0        100.0         0.0                 0.0            8
Count to Twenty-One                100.0          0.0         0.0                 0.0            8
Domineering                         50.0         50.0         0.0                 0.0            8
Grundy's Game                      100.0          0.0         0.0                 0.0            8
Kayles                             100.0          0.0         0.0                 0.0            8
Subtract a Square                  100.0          0.0         0.0                 0.0            8
Tic Tac Toe (3x4, 3-in-a-row)       75.0         25.0         0.0                 0.0            8
Tic Tac Toe (4x3, 3-in-a-row)       87.5          0.0        12.5                 0.0            8
Turning Turtles                     25.0         75.0         0.0                 0.0            8
Wythof's Nim                       100.0          0.0         0.0                 0.0            8

Overall Model Statistics:
================================================================================
Win Rate: 70.2%
Loss Rate: 28.8%
Draw Rate: 1.0%
Invalid Move Rate: 0.0%
Total Games: 104```

Performance from Qwen-235, with an average win rate of ~58%:
```
Game-specific Statistics:
================================================================================
                               wins_rate  losses_rate  draws_rate  invalid_moves_rate  total_games
game_name                                                                                         
Book Nim                            87.5          0.0         0.0                12.5            8
Coin Counter                         0.0        100.0         0.0                 0.0            8
Connect 3 (4x5)                     37.5         62.5         0.0                 0.0            8
Connect 3 (5x4)                     25.0         75.0         0.0                 0.0            8
Count to Twenty-One                100.0          0.0         0.0                 0.0            8
Domineering                         25.0         62.5         0.0                12.5            8
Grundy's Game                      100.0          0.0         0.0                 0.0            8
Kayles                              75.0         12.5         0.0                12.5            8
Subtract a Square                  100.0          0.0         0.0                 0.0            8
Tic Tac Toe (3x4, 3-in-a-row)       37.5         62.5         0.0                 0.0            8
Tic Tac Toe (4x3, 3-in-a-row)       87.5         12.5         0.0                 0.0            8
Turning Turtles                      0.0         87.5         0.0                12.5            8
Wythof's Nim                        87.5          0.0         0.0                12.5            8

Overall Model Statistics:
================================================================================
Win Rate: 58.7%
Loss Rate: 36.5%
Draw Rate: 0.0%
Invalid Move Rate: 4.8%
Total Games: 104```


Performance from GPT-4.1, with an average of 49% correct:
```
Game-specific Statistics:
================================================================================
                               wins_rate  losses_rate  draws_rate  invalid_moves_rate  total_games
game_name                                                                                         
Book Nim                            62.5         37.5         0.0                 0.0            8
Coin Counter                         0.0        100.0         0.0                 0.0            8
Connect 3 (4x5)                     87.5         12.5         0.0                 0.0            8
Connect 3 (5x4)                     25.0         75.0         0.0                 0.0            8
Count to Twenty-One                 25.0         62.5         0.0                12.5            8
Domineering                         12.5         87.5         0.0                 0.0            8
Grundy's Game                      100.0          0.0         0.0                 0.0            8
Kayles                             100.0          0.0         0.0                 0.0            8
Subtract a Square                  100.0          0.0         0.0                 0.0            8
Tic Tac Toe (3x4, 3-in-a-row)       25.0         75.0         0.0                 0.0            8
Tic Tac Toe (4x3, 3-in-a-row)       37.5         62.5         0.0                 0.0            8
Turning Turtles                      0.0        100.0         0.0                 0.0            8
Wythof's Nim                        62.5         37.5         0.0                 0.0            8

Overall Model Statistics:
================================================================================
Win Rate: 49.0%
Loss Rate: 50.0%
Draw Rate: 0.0%
Invalid Move Rate: 1.0%
Total Games: 104```


Per game performance from DeepSeekV3, with an average of ~45% correct:
```
Game-specific Statistics:
================================================================================
                               wins_rate  losses_rate  draws_rate  invalid_moves_rate  total_games
game_name                                                                                         
Book Nim                            12.5         87.5         0.0                 0.0            8
Coin Counter                         0.0        100.0         0.0                 0.0            8
Connect 3 (4x5)                      0.0        100.0         0.0                 0.0            8
Connect 3 (5x4)                      0.0        100.0         0.0                 0.0            8
Count to Twenty-One                 25.0         75.0         0.0                 0.0            8
Domineering                          0.0        100.0         0.0                 0.0            8
Grundy's Game                       62.5         37.5         0.0                 0.0            8
Kayles                             100.0          0.0         0.0                 0.0            8
Subtract a Square                   75.0         25.0         0.0                 0.0            8
Tic Tac Toe (3x4, 3-in-a-row)       50.0         50.0         0.0                 0.0            8
Tic Tac Toe (4x3, 3-in-a-row)       87.5         12.5         0.0                 0.0            8
Turning Turtles                     87.5         12.5         0.0                 0.0            8
Wythof's Nim                        87.5         12.5         0.0                 0.0            8

Overall Model Statistics:
================================================================================
Win Rate: 45.2%
Loss Rate: 54.8%
Draw Rate: 0.0%
Invalid Move Rate: 0.0%
Total Games: 104```

Per-game performance from Claude Sonnet 3.7, with an average of ~26% correct:

```
Game-specific Statistics:
================================================================================
                               wins_rate  losses_rate  draws_rate  invalid_moves_rate  total_games
game_name                                                                                         
Book Nim                             0.0        100.0         0.0                 0.0            8
Coin Counter                         0.0        100.0         0.0                 0.0            8
Connect 3 (4x5)                     12.5         87.5         0.0                 0.0            8
Connect 3 (5x4)                     12.5         87.5         0.0                 0.0            8
Count to Twenty-One                100.0          0.0         0.0                 0.0            8
Domineering                         25.0         75.0         0.0                 0.0            8
Grundy's Game                       12.5         87.5         0.0                 0.0            8
Kayles                               0.0        100.0         0.0                 0.0            8
Subtract a Square                   50.0         50.0         0.0                 0.0            8
Tic Tac Toe (3x4, 3-in-a-row)       62.5         37.5         0.0                 0.0            8
Tic Tac Toe (4x3, 3-in-a-row)       50.0         50.0         0.0                 0.0            8
Turning Turtles                      0.0        100.0         0.0                 0.0            8
Wythof's Nim                        12.5         87.5         0.0                 0.0            8

Overall Model Statistics:
================================================================================
Win Rate: 26.0%
Loss Rate: 74.0%
Draw Rate: 0.0%
Invalid Move Rate: 0.0%
Total Games: 104```
