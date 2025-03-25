import pytest
from games.tic_tac_toe_uneven import TicTacToeUnevenState

def test_initialization():
    # Test default initialization
    game = TicTacToeUnevenState()
    assert game.num_rows == 3
    assert game.num_cols == 4
    assert game.num_in_a_row == 3
    assert game.player_to_move == 0
    assert all(cell == '' for row in game.board for cell in row)

    # Test custom board size
    game = TicTacToeUnevenState(num_rows=4, num_cols=5, num_in_a_row=4)
    assert game.num_rows == 4
    assert game.num_cols == 5
    assert game.num_in_a_row == 4

    # Test custom board stuff remains same after a move
    game = game.take_action("0,0")
    assert game.num_rows == 4
    assert game.num_cols == 5
    assert game.num_in_a_row == 4

def test_legal_actions():

    for num_rows in range(3, 6):
        for num_cols in range(3, 6):
            game = TicTacToeUnevenState(num_rows=num_rows, num_cols=num_cols)
            # Initial board should have all positions available
            actions = game.get_legal_actions()
            assert len(actions) == num_rows * num_cols
            for row in range(num_rows):
                for col in range(num_cols):
                    assert f"{row},{col}" in actions

    # Test after making a move
    game = TicTacToeUnevenState(num_rows=3, num_cols=4, num_in_a_row=3)
    # Test after making a move
    game = game.take_action("1,1")
    actions = game.get_legal_actions()
    assert len(actions) == 11
    assert "1,1" not in actions

def test_take_action():
    game = TicTacToeUnevenState()
    
    # Test valid moves
    game = game.take_action("0,0")
    assert game.board[0][0] == 'X'
    assert game.player_to_move == 1
    
    game = game.take_action("1,1")
    assert game.board[1][1] == 'O'
    assert game.player_to_move == 0

    # Test invalid moves
    with pytest.raises(ValueError):
        game.take_action("0,0")  # Already occupied
    with pytest.raises(ValueError):
        game.take_action("3,4")  # Out of bounds

def test_win_conditions():
    # Test horizontal win
    game = TicTacToeUnevenState()
    moves = ["0,0", "1,0", "0,1", "1,1", "0,2"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins

    # Test vertical win
    game = TicTacToeUnevenState()
    moves = ["0,0", "0,1", "1,0", "0,2", "2,0"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins

    # Test diagonal win (down-right)
    game = TicTacToeUnevenState()
    moves = ["0,0", "0,1", "1,1", "0,2", "2,2"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins

    # Test diagonal win (down-left)
    game = TicTacToeUnevenState()
    moves = ["0,2", "0,1", "1,1", "0,0", "2,0"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins

    # Do the above, just with a 4x4 board and 4-in-a-row

    # Horizontal win
    game = TicTacToeUnevenState(num_rows=4, num_cols=4, num_in_a_row=4)
    moves = ["0,0", "1,0", "0,1", "1,1", "0,2", "1,2", "0,3"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins
    
    # Vertical win
    game = TicTacToeUnevenState(num_rows=4, num_cols=4, num_in_a_row=4)
    moves = ["0,0", "0,1", "1,0", "0,2", "2,0", "0,3", "3,0"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins

    # Diagonal win (down-right)
    game = TicTacToeUnevenState(num_rows=4, num_cols=4, num_in_a_row=4)
    moves = ["0,0", "0,1", "1,1", "0,2", "2,2", "0,3", "3,3"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins

    # Diagonal win (down-left)
    game = TicTacToeUnevenState(num_rows=4, num_cols=4, num_in_a_row=4)
    moves = ["0,3", "0,1", "1,2", "0,2", "2,1", "0,0", "3,0"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (1.0, -1.0)  # Player 0 wins
    

def test_draw_game():
    game = TicTacToeUnevenState(num_rows=3, num_cols=3, num_in_a_row=3)
    # Fill board without any wins
    moves = ["1,1", "0,0", "2,2", "0,2", "0,1", "2,1", "2,0", "1,0", "1,2"]
    for move in moves:
        game = game.take_action(move)
    assert game.is_terminal()
    assert game.get_result() == (0.0, 0.0)  # Draw

def test_game_descriptions():
    game = TicTacToeUnevenState(num_rows=3, num_cols=4, num_in_a_row=3)
    assert "3 x 4" in game.get_name()
    assert "3-in-a-row" in game.get_name()
    assert "3 x 4" in game.get_short_game_description()
    assert "3-in-a-row" in game.get_detailed_rules()
    
def test_string_representation():
    game = TicTacToeUnevenState()
    game = game.take_action("0,0")
    game = game.take_action("1,1")
    str_rep = str(game)
    assert "X" in str_rep
    assert "O" in str_rep
    assert "Player 0's turn" in str_rep

def test_all():
    test_initialization()
    test_legal_actions()
    test_take_action()
    test_win_conditions()
    test_draw_game()
    test_game_descriptions()