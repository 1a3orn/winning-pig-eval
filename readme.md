To run

python src/play.py --model_name [model_name] --num_games [num_games]

See src/llms/get_llm.py for how to add models and how to add model names.

Per game performance from DeepSeekV3, with an average of ~45% correct:
```
Statistics by Game:
================================================================================
                               Win Rate (%)  Draw Rate (%)  Loss Rate (%)  Invalid Move Rate (%)  Total Games
game_name                                                                                                    
Book Nim                              12.50           0.00          87.50                   0.00            8
Coin Counter                           0.00           0.00         100.00                   0.00            8
Connect 3 (4x5)                        0.00           0.00         100.00                   0.00            8
Connect 3 (5x4)                        0.00           0.00         100.00                   0.00            8
Count to Twenty-One                   25.00           0.00          75.00                   0.00            8
Domineering                            0.00           0.00         100.00                   0.00            8
Grundy's Game                         62.50           0.00          37.50                   0.00            8
Kayles                               100.00           0.00           0.00                   0.00            8
Subtract a Square                     75.00           0.00          25.00                   0.00            8
Tic Tac Toe (3x4, 3-in-a-row)         50.00           0.00          50.00                   0.00            8
Tic Tac Toe (4x3, 3-in-a-row)         87.50           0.00          12.50                   0.00            8
Turning Turtles                       87.50           0.00          12.50                   0.00            8
Wythof's Nim                          87.50           0.00          12.50                   0.00            8
```

Per-game performance from Claude Sonnet 3.7, the next best performing model, with an average of ~25% correct:

```

Statistics by Game:
================================================================================
                               Win Rate (%)  Draw Rate (%)  Loss Rate (%)  Invalid Move Rate (%)  Total Games
game_name                                                                                                    
Book Nim                               0.00           0.00         100.00                   0.00            8
Coin Counter                           0.00           0.00         100.00                   0.00            8
Connect 3 (4x5)                       12.50           0.00          87.50                   0.00            8
Connect 3 (5x4)                       12.50           0.00          87.50                   0.00            8
Count to Twenty-One                  100.00           0.00           0.00                   0.00            8
Domineering                           25.00           0.00          75.00                   0.00            8
Grundy's Game                         12.50           0.00          87.50                   0.00            8
Kayles                                 0.00           0.00         100.00                   0.00            8
Subtract a Square                     50.00           0.00          50.00                   0.00            8
Tic Tac Toe (3x4, 3-in-a-row)         62.50           0.00          37.50                   0.00            8
Tic Tac Toe (4x3, 3-in-a-row)         50.00           0.00          50.00                   0.00            8
Turning Turtles                        0.00           0.00         100.00                   0.00            8
Wythof's Nim                          12.50           0.00          87.50                   0.00            8
```

You'll note they do well on different games; Claude gets 100% on Count to 21 and 0% on Kayles, while DeepSeek does the reverse.