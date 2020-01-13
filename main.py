import numpy as np
from piece import Piece

# print(help(Piece))
# isinstance()
# issubclass()
# "dunder" ==> __ __
# return NotImplemented
# @property
# def instanceMethod(self):
#   ...

# @instanceMethod.setter
# def instanceMethod(self, input):
#   "modify input"
#   self.someProperty = "modified input"


def setup_board(board):
    '''
    Setup the board by populating it with Piece objects
    '''
    for i in range(4):
        # Add black pieces
        board[0][1 + 2*i] = Piece((1 + 2*i, 0), False)
        board[2][1 + 2*i] = Piece((1 + 2*i, 2), False)
        board[1][2*i] = Piece((2*i, 1), False)
        # Add white pieces
        board[5][2*i] = Piece((2*i, 5))
        board[7][2*i] = Piece((2*i, 7))
        board[6][1 + 2*i] = Piece((1 + 2*i, 6))


def display_board(board):
    """
    Takes a board object and displays the current game state
    in the commandline.
    Args:
    board -> List(Piece, Int)
    Returns:
    None
    """
    for row in board:
        for item in row:
            if item == 0:
                print("| |", end="")
            else:
                if item.white:
                    print("|X|", end="")
                else:
                    print("|O|", end="")
        print()


def get_moves(board, white_turn):
    """
    Takes a board object and a boolean representing which players turn it is
    and returns a list of tuples representing what legal moves can be made
    given the gamestate.
    Args:
    board -> List[Piece, Int]
    white_turn -> Bool
    Returns:
    legal_moves -> List[Tuple(Tuple, List[Tuple])]
    """

    # Get all pieces and flatten to a 1d list
    all_pieces = [piece for row in [[item for item in row if isinstance(
        item, Piece)] for row in board] for piece in row]

    if white_turn:
        # Get white pieces
        pieces = [piece for piece in all_pieces if piece.white]
    else:
        # Get black pieces
        pieces = [piece for piece in all_pieces if not piece.white]

    move_info = []
    # Check for possible moves for pieces of a given color
    for piece in pieces:
        moves = piece.potential_moves(board)
        # If the piece can move add its position and a list of its moves to move_info
        if moves != None:
            move_info.append(((piece.x, piece.y), moves))

    # Only count capturing moves as legal moves if such capturing moves exist.
    capturing_moves = [(info[0], info[1][0], info[1][1])
                       for info in move_info if info[1][0] == True]
    if len(capturing_moves) > 0:
        legal_moves = capturing_moves
    else:
        legal_moves = [(info[0], info[1][0], info[1][1])
                       for info in move_info if info[1][0] == False]

    return legal_moves


def player_input(moves):
    """
    Takes a moves object and asks the players two questions to determine
    the piece they wish to move and the move they wish to make with that
    piece. Returns a tuple containing their selection.
    Args:
    moves -> List[Tuple(x,y), Bool, List[Tuple(x,y)]]
    Returns:
    Tuple(Int)
    """
    print("Pieces that can move: ", [piece[0] for piece in moves])
    # Get player input
    selected_piece = int(input(
        f"Select a piece to move by typing a number between 0 and {len(moves) - 1}: "))
    print("Possible moves: ", moves[selected_piece][2])
    selected_move = int(input(
        f"Select a move by typing a number between 0 and {len(moves[selected_piece][2]) - 1}: "))
    return (selected_piece, selected_move)


def move(board, pos, new_pos, made_capture):
    return None


# board for testing double capture scenarios
test_board1 = [[0 for _ in range(8)] for _ in range(8)]
test_board1[0][7] = Piece((7, 0), False)
test_board1[1][2] = Piece((2, 1), False)
test_board1[1][6] = Piece((6, 1), False)
test_board1[2][5] = Piece((5, 2))
test_board1[3][4] = Piece((4, 3))
test_board1[4][3] = Piece((3, 4))
test_board1[6][3] = Piece((3, 6))


def main():
    # # A 2d array to store the pieces
    # board = [[0 for _ in range(8)] for _ in range(8)]
    # # Populate the board with piece objects - 0 indicates an empty field
    # setup_board(board)

    board = test_board1

    game_over = False
    white_turn = True

    # Game loop
    while not game_over:

        turn_ongoing = True
        while turn_ongoing:
            display_board(board)
            if white_turn:
                print("White to play")
            else:
                print("Black to play")

            # Get moves given game state and turn
            moves = get_moves(board, white_turn)

            # Get player input
            selected_piece, selected_move = player_input(moves)

            # Get info about the desired move
            x, y = moves[selected_piece][0]
            new_x, new_y = moves[selected_piece][2][selected_move]
            capturing_move = moves[selected_piece][1]
            # Move the piece accordingly
            piece = board[y][x]
            board[new_y][new_x] = piece
            board[y][x] = 0
            # Update the position, check for promotion to king
            piece.update((new_x, new_y))
            # If piece made a capture check if any new captures must be made
            if capturing_move:
                # Remove the captured piece from the board
                dx, dy = new_x - x, new_y - y
                captured_x, captured_y = x + int(dx / 2), y + int(dy / 2)
                board[captured_y][captured_x] = 0

                # If piece can still move
                if piece.potential_moves(board) != None:
                    can_capture, piece_moves = piece.potential_moves(board)
                    # If it cannot make any more captures end the turn
                    if not can_capture:
                        # FIX: In a scenario where one piece can make a double capture and another a single and
                        # the player selects the double capture, this won't ensure that the double capture occurs.
                        # we must ensure that upon a capture only the possible moves of the piece which captures are
                        # checked. This can be illustrated with the test board
                        turn_ongoing = False
                # If no subsequent captures can be made with the piece end the players turn
                else:
                    turn_ongoing = False
            else:
                turn_ongoing = False
        white_turn = not white_turn


if __name__ == "__main__":
    main()
